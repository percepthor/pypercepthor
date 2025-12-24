"""Property tests of the validators and the body reader with hypothesis.

Any bytes from the client end in the value, in its error or in nothing, never in an
exception that would answer 500 from the route. The number of examples comes from
the profile: ci in the default runs, nightly with ./run.sh fuzz.
"""

import json
import pytest
from hypothesis import given
from hypothesis import strategies
from unittest.mock import patch

from percepthor.validations import bodies, queries
from percepthor.validations import percepthor_handle_body_input
from percepthor.validations import percepthor_query_bool_value_from_params
from percepthor.validations import percepthor_query_float_value_from_params
from percepthor.validations import percepthor_query_int_value_from_params
from percepthor.validations import percepthor_query_optional_value_from_params
from percepthor.validations import percepthor_query_value_from_params

from shared import build_string

pytestmark = [pytest.mark.unit, pytest.mark.fuzz]

FIELD = "field"

PARAMS = None
REQUEST = None

REQUIRED_VALIDATORS = (
	percepthor_query_value_from_params,
	percepthor_query_int_value_from_params,
	percepthor_query_float_value_from_params,
	percepthor_query_bool_value_from_params
)

def _handle_input (loaded_json: dict, errors: dict) -> dict:
	return loaded_json

class TestQueryFuzz:

	@given (value=strategies.binary ())
	def test_required_validators_end_in_a_value_or_an_error (self, value):
		for validator in REQUIRED_VALIDATORS:
			query = dict ()
			errors = dict ()

			with patch.object (queries, "http_query_pairs_get_value", return_value=build_string (value)):
				validator (query, PARAMS, FIELD, errors)

			assert (FIELD in query) != (FIELD in errors)

	@given (value=strategies.binary ())
	def test_optional_value_never_raises (self, value):
		query = dict ()

		with patch.object (queries, "http_query_pairs_get_value", return_value=build_string (value)):
			percepthor_query_optional_value_from_params (query, PARAMS, FIELD)

		assert set (query) <= {FIELD}

class TestBodyFuzz:

	@given (content=strategies.binary ())
	def test_any_body_ends_in_values_or_an_error (self, content):
		errors = dict ()

		with patch.object (bodies, "http_request_get_body", return_value=build_string (content)):
			values = percepthor_handle_body_input (REQUEST, _handle_input, errors)

		assert (values is None) == ("body" in errors)
		assert (values is None) or isinstance (values, dict)

	@given (body=strategies.dictionaries (strategies.text (), strategies.text () | strategies.integers ()))
	def test_any_object_reaches_the_input_handler (self, body):
		errors = dict ()
		content = json.dumps (body).encode ("utf-8")

		with patch.object (bodies, "http_request_get_body", return_value=build_string (content)):
			values = percepthor_handle_body_input (REQUEST, _handle_input, errors)

		assert values == body
		assert not errors
