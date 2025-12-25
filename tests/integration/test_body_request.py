"""The body reader over a real request of libcerver.

A request created by libcerver without a body returns the real NULL String of
http_request_get_body (), the case that answered 500: nothing of cerver is patched.

Bugs these tests fixed:
- a request without a body answered 500: a NULL ctypes pointer is not None
"""

import pytest
from ctypes import c_void_p

from cerver.lib import lib

from percepthor import percepthor_handle_body_input

pytestmark = [pytest.mark.integration]

BODY_ERROR_REQUIRED = "Request body input is required!"

http_request_new = lib.http_request_new
http_request_new.restype = c_void_p

http_request_delete = lib.http_request_delete
http_request_delete.argtypes = [c_void_p]

@pytest.fixture
def request_without_body ():
	request = http_request_new ()

	yield request

	http_request_delete (request)

class TestBodyRequest:

	def test_request_without_body_is_required (self, request_without_body):
		handled = list ()
		errors = dict ()

		values = percepthor_handle_body_input (
			request_without_body, lambda loaded_json, input_errors: handled.append (loaded_json), errors
		)

		assert values is None
		assert errors == {"body": BODY_ERROR_REQUIRED}
		assert not handled
