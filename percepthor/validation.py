from ctypes import POINTER, c_void_p
import distutils.util
import json
from typing import Any, Callable

from cerver.types import String

from cerver.http import http_query_pairs_get_value
from cerver.http import http_request_get_body

def percepthor_query_value_from_params (
	query: dict, params: c_void_p, name: str, errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = found.contents.str.decode ("utf-8")

		except:
			errors[name] = f"Field {name} is invalid."

	else:
		errors[name] = f"Field {name} is required."

def percepthor_query_value_from_params_with_cast (
	query: dict, params: c_void_p, name: str, cast: Callable [[str], Any], errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = cast (found.contents.str.decode ("utf-8"))

		except:
			errors[name] = f"Field {name} is invalid."

	else:
		errors[name] = f"Field {name} is required."

def percepthor_query_optional_value_from_params (
	query: dict, params: c_void_p, name: str
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		query[name] = found.contents.str.decode ("utf-8")

def percepthor_query_optional_value_from_params_with_cast (
	query: dict, params: c_void_p, name: str, cast: Callable [[str], Any], errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = cast (found.contents.str.decode ("utf-8"))

		except:
			errors[name] = f"Field {name} is invalid."

def percepthor_query_int_value_from_params (
	query: dict, params: c_void_p, name: str, errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = int (found.contents.str.decode ("utf-8"))
		except ValueError:
			errors[name] = f"Field {name} is invalid."

	else:
		errors[name] = f"Field {name} is required."

def percepthor_query_int_optional_value_from_params (
	query: dict, params: c_void_p, name: str, errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = int (found.contents.str.decode ("utf-8"))
		except ValueError:
			errors[name] = f"Field {name} is invalid."

def percepthor_query_int_value_from_params_with_default (
	query: dict, params: c_void_p, name: str, default: int
):
	query[name] = default

	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = int (found.contents.str.decode ("utf-8"))
		except ValueError:
			pass

def percepthor_query_float_value_from_params (
	query: dict, params: c_void_p, name: str, errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = float (found.contents.str.decode ("utf-8"))
		except ValueError:
			errors[name] = f"Field {name} is invalid."

	else:
		errors[name] = f"Field {name} is required."

def percepthor_query_float_optional_value_from_params (
	query: dict, params: c_void_p, name: str, errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = float (found.contents.str.decode ("utf-8"))
		except ValueError:
			errors[name] = f"Field {name} is invalid."

def percepthor_query_float_value_from_params_with_default (
	query: dict, params: c_void_p, name: str, default: float
):
	query[name] = default

	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = float (found.contents.str.decode ("utf-8"))
		except ValueError:
			pass

def percepthor_query_bool_value_from_params (
	query: dict, params: c_void_p, name: str, errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = bool (
				distutils.util.strtobool (found.contents.str.decode ("utf-8"))
			)
		except ValueError:
			errors[name] = f"Field {name} is invalid."

	else:
		errors[name] = f"Field {name} is required."

def percepthor_query_bool_optional_value_from_params (
	query: dict, params: c_void_p, name: str, errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = bool (
				distutils.util.strtobool (found.contents.str.decode ("utf-8"))
			)
		except ValueError:
			errors[name] = f"Field {name} is invalid."

def percepthor_handle_body_input (
	request: c_void_p, handle_body_input: Callable [[dict, dict], dict], errors: dict
) -> dict:
	values = None

	body_json: POINTER (String) = http_request_get_body (request)

	if (body_json is not None):
		loaded_json: dict = json.loads (body_json.contents.str)

		handle_body_input (loaded_json, errors)

	else:
		errors["body"] = "Request body input is required!"

	return values
