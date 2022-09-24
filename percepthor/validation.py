from ctypes import c_void_p
import distutils.util
from typing import Any, Callable

from cerver.http import http_query_pairs_get_value

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
	query: dict, params: c_void_p, name: str, cast: Callable (Any), errors: dict
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
	query: dict, params: c_void_p, name: str, cast: Callable (Any), errors: dict
):
	found = http_query_pairs_get_value (params, name.encode ("utf-8"))
	if (found):
		try:
			query[name] = cast (found.contents.str.decode ("utf-8"))

		except:
			errors[name] = f"Field {name} is invalid."

def validate_query_value_with_cast (
	values: c_void_p, query_name: str, cast: Callable (Any), errors: dict
):
	result = None

	found = http_query_pairs_get_value (values, query_name.encode ("utf-8"))
	if (found):
		try:
			query_value = found.contents.str.decode ("utf-8")

			result = cast (query_value)

		except:
			errors[query_name] = f"Field {query_name} is invalid."

	return result

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
