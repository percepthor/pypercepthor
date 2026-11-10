"""Unit tests for the validations - the query validators and the body reader.

cerver's getters are patched where the validators use them (percepthor.validations.queries
and .bodies), to real cerver Strings or to a real NULL pointer, which is what libcerver
returns. Every validator either writes its value, writes its error, or writes nothing for
an optional value; none raises into the route.

Bugs these tests fixed:
- a request without a body answered 500: a NULL ctypes pointer is not None
- a body that was not json, or a json that was not an object, answered 500
- an optional query value that was not utf-8 raised UnicodeDecodeError
- a body and a query value were read up to their first NUL byte instead of their length
- an integer with a default that was not utf-8 raised UnicodeDecodeError
"""

import json
import pytest
from unittest.mock import patch

from percepthor.validations import bodies, queries
from percepthor.validations import percepthor_body_json_load
from percepthor.validations import percepthor_handle_body_input
from percepthor.validations import percepthor_query_bool_optional_value_from_params
from percepthor.validations import percepthor_query_bool_value_from_params
from percepthor.validations import percepthor_query_float_optional_value_from_params
from percepthor.validations import percepthor_query_float_value_from_params
from percepthor.validations import percepthor_query_float_value_from_params_with_default
from percepthor.validations import percepthor_query_int_optional_value_from_params
from percepthor.validations import percepthor_query_int_value_from_params
from percepthor.validations import percepthor_query_int_value_from_params_with_default
from percepthor.validations import percepthor_query_optional_value_from_params
from percepthor.validations import percepthor_query_optional_value_from_params_with_cast
from percepthor.validations import percepthor_query_value_from_params
from percepthor.validations import percepthor_query_value_from_params_with_cast

from shared import build_null_string
from shared import build_string

pytestmark = [pytest.mark.unit]

FIELD = "skip"

PARAMS = None
REQUEST = None

INT_DEFAULT = 7
FLOAT_DEFAULT = 1.5

NOT_UTF8 = b"\xff\xfe"

ERROR_REQUIRED = f"Field {FIELD} is required."
ERROR_INVALID = f"Field {FIELD} is invalid."

BODY_ERROR_REQUIRED = "Request body input is required!"
BODY_ERROR_INVALID = "Request body input is invalid."

def _query (value):
	"""Patches the query getter of cerver to return the value, bytes or None for a missing one."""
	found = build_null_string () if (value is None) else build_string (value)

	return patch.object (queries, "http_query_pairs_get_value", return_value=found)

def _takes_errors (validator) -> bool:
	"""The validators with a default do not take the errors."""
	return validator.__code__.co_varnames[validator.__code__.co_argcount - 1] == "errors"

def _run (validator, value, *args):
	"""Runs a query validator over the value, with the arguments that follow the name."""
	query = dict ()
	errors = dict ()

	with _query (value):
		if (_takes_errors (validator)):
			validator (query, PARAMS, FIELD, *args, errors)

		else:
			validator (query, PARAMS, FIELD, *args)

	return query, errors

class TestRequiredValues:

	def test_value (self):
		query, errors = _run (percepthor_query_value_from_params, b"10")
		assert query == {FIELD: "10"}
		assert not errors

	def test_missing_value_is_required (self):
		query, errors = _run (percepthor_query_value_from_params, None)
		assert not query
		assert errors == {FIELD: ERROR_REQUIRED}

	def test_value_that_is_not_utf8_is_invalid (self):
		query, errors = _run (percepthor_query_value_from_params, NOT_UTF8)
		assert errors == {FIELD: ERROR_INVALID}

	def test_value_with_cast (self):
		query, errors = _run (percepthor_query_value_from_params_with_cast, b"10", int)
		assert query == {FIELD: 10}

	def test_value_with_cast_that_fails_is_invalid (self):
		query, errors = _run (percepthor_query_value_from_params_with_cast, b"ten", int)
		assert errors == {FIELD: ERROR_INVALID}

	def test_missing_value_with_cast_is_required (self):
		query, errors = _run (percepthor_query_value_from_params_with_cast, None, int)
		assert errors == {FIELD: ERROR_REQUIRED}

class TestOptionalValues:

	def test_value (self):
		query, errors = _run (percepthor_query_optional_value_from_params, b"10")
		assert query == {FIELD: "10"}

	def test_missing_value_is_left_out (self):
		query, errors = _run (percepthor_query_optional_value_from_params, None)
		assert not query
		assert not errors

	def test_value_that_is_not_utf8_is_left_out (self):
		query, errors = _run (percepthor_query_optional_value_from_params, NOT_UTF8)
		assert not query

	def test_value_with_cast (self):
		query, errors = _run (percepthor_query_optional_value_from_params_with_cast, b"10", int)
		assert query == {FIELD: 10}

	def test_value_with_cast_that_fails_is_invalid (self):
		query, errors = _run (percepthor_query_optional_value_from_params_with_cast, b"ten", int)
		assert errors == {FIELD: ERROR_INVALID}

	def test_missing_value_with_cast_is_left_out (self):
		query, errors = _run (percepthor_query_optional_value_from_params_with_cast, None, int)
		assert not query
		assert not errors

	def test_value_that_is_not_utf8_without_errors_is_left_out (self):
		query = dict ()

		with _query (NOT_UTF8):
			percepthor_query_optional_value_from_params (query, PARAMS, FIELD)

		assert not query

	def test_value_that_is_not_utf8_with_errors_is_invalid (self):
		query, errors = _run (percepthor_query_optional_value_from_params, NOT_UTF8)
		assert errors == {FIELD: ERROR_INVALID}

class CastError (Exception):
	"""An error of a cast that is not a ValueError, like the InvalidId of an ObjectId."""

def _cast_that_fails (value: str):
	raise CastError (value)

class TestCasts:

	@pytest.mark.parametrize ("validator", [
		percepthor_query_value_from_params_with_cast,
		percepthor_query_optional_value_from_params_with_cast
	])
	def test_any_error_of_a_cast_is_invalid (self, validator):
		query, errors = _run (validator, b"value", _cast_that_fails)
		assert not query
		assert errors == {FIELD: ERROR_INVALID}

	def test_value_with_a_nul_byte_is_read_whole (self):
		query, errors = _run (percepthor_query_value_from_params, b"a\x00b")
		assert query == {FIELD: "a\x00b"}

	def test_default_of_a_value_that_is_not_utf8 (self):
		query = dict ()

		with _query (NOT_UTF8):
			percepthor_query_int_value_from_params_with_default (query, PARAMS, FIELD, INT_DEFAULT)

		assert query == {FIELD: INT_DEFAULT}

class TestNumbers:

	@pytest.mark.parametrize ("validator, value, expected", [
		(percepthor_query_int_value_from_params, b"-3", -3),
		(percepthor_query_int_optional_value_from_params, b"3", 3),
		(percepthor_query_float_value_from_params, b"2.5", 2.5),
		(percepthor_query_float_optional_value_from_params, b"-2.5", -2.5)
	])
	def test_value (self, validator, value, expected):
		query, errors = _run (validator, value)
		assert query == {FIELD: expected}
		assert not errors

	@pytest.mark.parametrize ("validator", [
		percepthor_query_int_value_from_params,
		percepthor_query_int_optional_value_from_params,
		percepthor_query_float_value_from_params,
		percepthor_query_float_optional_value_from_params
	])
	@pytest.mark.parametrize ("value", [b"ten", b"", NOT_UTF8])
	def test_invalid_value (self, validator, value):
		query, errors = _run (validator, value)
		assert not query
		assert errors == {FIELD: ERROR_INVALID}

	@pytest.mark.parametrize ("validator", [
		percepthor_query_int_value_from_params,
		percepthor_query_float_value_from_params
	])
	def test_missing_value_is_required (self, validator):
		query, errors = _run (validator, None)
		assert errors == {FIELD: ERROR_REQUIRED}

	@pytest.mark.parametrize ("validator", [
		percepthor_query_int_optional_value_from_params,
		percepthor_query_float_optional_value_from_params
	])
	def test_missing_optional_value_is_left_out (self, validator):
		query, errors = _run (validator, None)
		assert not query
		assert not errors

	@pytest.mark.parametrize ("validator, default, value, expected", [
		(percepthor_query_int_value_from_params_with_default, INT_DEFAULT, b"3", 3),
		(percepthor_query_int_value_from_params_with_default, INT_DEFAULT, b"ten", INT_DEFAULT),
		(percepthor_query_int_value_from_params_with_default, INT_DEFAULT, None, INT_DEFAULT),
		(percepthor_query_float_value_from_params_with_default, FLOAT_DEFAULT, b"0.5", 0.5),
		(percepthor_query_float_value_from_params_with_default, FLOAT_DEFAULT, b"half", FLOAT_DEFAULT),
		(percepthor_query_float_value_from_params_with_default, FLOAT_DEFAULT, None, FLOAT_DEFAULT)
	])
	def test_value_with_default (self, validator, default, value, expected):
		query = dict ()

		with _query (value):
			validator (query, PARAMS, FIELD, default)

		assert query == {FIELD: expected}

class TestBooleans:

	@pytest.mark.parametrize ("value, expected", [
		(b"true", True), (b"1", True), (b"yes", True), (b"on", True),
		(b"false", False), (b"0", False), (b"no", False), (b"off", False)
	])
	@pytest.mark.parametrize ("validator", [
		percepthor_query_bool_value_from_params,
		percepthor_query_bool_optional_value_from_params
	])
	def test_value (self, validator, value, expected):
		query, errors = _run (validator, value)
		assert query == {FIELD: expected}

	@pytest.mark.parametrize ("validator", [
		percepthor_query_bool_value_from_params,
		percepthor_query_bool_optional_value_from_params
	])
	@pytest.mark.parametrize ("value", [b"maybe", b"", NOT_UTF8])
	def test_invalid_value (self, validator, value):
		query, errors = _run (validator, value)
		assert errors == {FIELD: ERROR_INVALID}

	def test_missing_value_is_required (self):
		query, errors = _run (percepthor_query_bool_value_from_params, None)
		assert errors == {FIELD: ERROR_REQUIRED}

	def test_missing_optional_value_is_left_out (self):
		query, errors = _run (percepthor_query_bool_optional_value_from_params, None)
		assert not query
		assert not errors

def _read_body (body):
	"""Runs the real body reader over a body pointer, with an input handler that records its calls."""
	handled = list ()
	errors = dict ()

	def handle_input (loaded_json: dict, input_errors: dict) -> dict:
		handled.append (loaded_json)

		return {"values": loaded_json}

	with patch.object (bodies, "http_request_get_body", return_value=body):
		values = percepthor_handle_body_input (REQUEST, handle_input, errors)

	return values, errors, handled

class TestBodyInput:

	def test_missing_body_is_required (self):
		values, errors, handled = _read_body (build_null_string ())

		assert values is None
		assert errors == {"body": BODY_ERROR_REQUIRED}
		assert not handled

	@pytest.mark.parametrize ("content", [b"{", b"not json", NOT_UTF8, b""])
	def test_body_that_is_not_json_is_invalid (self, content):
		values, errors, handled = _read_body (build_string (content))

		assert values is None
		assert errors == {"body": BODY_ERROR_INVALID}
		assert not handled

	@pytest.mark.parametrize ("content", [b"null", b"[1]", b"\"text\"", b"5", b"true"])
	def test_json_that_is_not_an_object_is_invalid (self, content):
		values, errors, handled = _read_body (build_string (content))

		assert values is None
		assert errors == {"body": BODY_ERROR_INVALID}
		assert not handled

	def test_object_reaches_the_input_handler (self):
		body = {"name": "ñandú", "count": 2}

		values, errors, handled = _read_body (build_string (json.dumps (body).encode ("utf-8")))

		assert values == {"values": body}
		assert not errors
		assert handled == [body]

	def test_body_with_a_nul_byte_is_read_whole (self):
		# cut at its NUL, the body would be the valid object {"a": 1}
		values, errors, handled = _read_body (build_string (b"{\"a\": 1}\x00{\"b\": 2}"))

		assert values is None
		assert errors == {"body": BODY_ERROR_INVALID}
		assert not handled

	def test_empty_object_reaches_the_input_handler (self):
		values, errors, handled = _read_body (build_string (b"{}"))

		assert values == {"values": dict ()}
		assert handled == [dict ()]

class TestBodyJsonLoad:

	def test_object (self):
		errors = dict ()
		assert percepthor_body_json_load (build_string (b"{\"a\": 1}"), errors) == {"a": 1}
		assert not errors

	def test_not_an_object (self):
		errors = dict ()
		assert percepthor_body_json_load (build_string (b"[]"), errors) is None
		assert errors == {"body": BODY_ERROR_INVALID}
