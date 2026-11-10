"""The JSON body of a request, read and handed to the validator of the route.

The body is read with its length, so a body with a NUL byte is read whole (and is not
valid JSON) instead of being cut at it.
"""

import json
from typing import Any, Callable

from cerver.http import http_request_get_body
from cerver.types import string_bytes

__all__ = [
	"BODY_REQUIRED", "BODY_INVALID",
	"percepthor_body_json_load", "percepthor_handle_body_input"
]

BODY_REQUIRED = "Request body input is required!"
BODY_INVALID = "Request body input is invalid."

# a body that is not utf-8 or not json fails with one of these
BODY_DECODE_ERRORS = (ValueError, UnicodeDecodeError)

def percepthor_body_json_load (body_json: Any, errors: dict) -> dict | None:
	"""Loads the JSON object of a body.

	Args:
		body_json: The StringPointer of the body (http_request_get_body ()).
		errors: The errors of the request, "body" when it is not a JSON object.

	Returns:
		The object, None when the body is not one.
	"""
	loaded_json = None

	try:
		loaded_json = json.loads (string_bytes (body_json))

	except BODY_DECODE_ERRORS:
		pass

	if (not isinstance (loaded_json, dict)):
		loaded_json = None
		errors["body"] = BODY_INVALID

	return loaded_json

def percepthor_handle_body_input (
	request: int, handle_body_input: Callable [[dict, dict], Any], errors: dict
) -> Any:
	"""Reads the JSON body of a request and validates it.

	Args:
		request: The request.
		handle_body_input: The validator of the route, called with the body and the errors;
			it returns the values of the request.
		errors: The errors of the request, "body" when it is missing or is not a JSON object.

	Returns:
		What the validator returned, None when the body is missing or is not a JSON object.
	"""
	values = None

	body_json = http_request_get_body (request)

	# a NULL pointer of ctypes is falsy, never None
	if (body_json):
		loaded_json = percepthor_body_json_load (body_json, errors)

		if (loaded_json is not None):
			values = handle_body_input (loaded_json, errors)

	else:
		errors["body"] = BODY_REQUIRED

	return values
