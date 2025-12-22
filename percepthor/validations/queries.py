"""The validators of the values of a query, that write the values in a dict and the
errors of the request in another one.

The values are read with their length, so a value with a NUL byte is read whole, and a
value that is not utf-8 is invalid. The typed validators of pycerver
(``cerver.http.validate_query_*``) return the values instead of writing them.
"""

from typing import Any, Callable

from cerver.http import http_query_pairs_get_value
from cerver.types import string_bytes
from cerver.utils import strtobool

__all__ = [
	"QUERY_REQUIRED", "QUERY_INVALID",
	"percepthor_query_value_from_params", "percepthor_query_value_from_params_with_cast",
	"percepthor_query_optional_value_from_params", "percepthor_query_optional_value_from_params_with_cast",
	"percepthor_query_int_value_from_params", "percepthor_query_int_optional_value_from_params",
	"percepthor_query_int_value_from_params_with_default",
	"percepthor_query_float_value_from_params", "percepthor_query_float_optional_value_from_params",
	"percepthor_query_float_value_from_params_with_default",
	"percepthor_query_bool_value_from_params", "percepthor_query_bool_optional_value_from_params"
]

QUERY_REQUIRED = "Field {name} is required."
QUERY_INVALID = "Field {name} is invalid."

TEXT_ENCODING = "utf-8"

# a cast of the caller can fail with any error, like the InvalidId of an ObjectId,
# and the value is then invalid; KeyboardInterrupt and SystemExit are not errors of a value
QUERY_CAST_ERRORS = (Exception,)

class QueryMissing:
	"""The value of a key that the query does not have."""

QUERY_MISSING = QueryMissing ()

def query_text (params: int, name: str) -> Any:
	"""Returns the text of a value of the query.

	Raises:
		UnicodeDecodeError: If the value is not utf-8.

	Returns:
		The text, QUERY_MISSING when the query does not have the key.
	"""
	result = QUERY_MISSING

	value = string_bytes (http_query_pairs_get_value (params, name.encode (TEXT_ENCODING)))
	if (value is not None):
		result = value.decode (TEXT_ENCODING)

	return result

def query_cast (
	query: dict, params: int, name: str, cast: Callable [[str], Any],
	errors: dict | None, required: bool
) -> None:
	"""Writes the value of a key converted by cast, or its error.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		cast: Converts the text of the value.
		errors: The errors of the request, None to leave an invalid value out without an error.
		required: True to write the required error of a missing value.
	"""
	try:
		text = query_text (params, name)
		if (text is not QUERY_MISSING):
			query[name] = cast (text)

		elif (required and (errors is not None)):
			errors[name] = QUERY_REQUIRED.format (name=name)

	except QUERY_CAST_ERRORS:
		if (errors is not None):
			errors[name] = QUERY_INVALID.format (name=name)

def query_default (query: dict, params: int, name: str, cast: Callable [[str], Any], default: Any) -> None:
	"""Writes the value of a key converted by cast, or the default when it is missing or invalid."""
	query[name] = default

	query_cast (query, params, name, cast, None, False)

def query_bool (text: str) -> bool:
	"""Converts the text of a truth value, like "true", "yes" or "0"."""
	return bool (strtobool (text))

def percepthor_query_value_from_params (query: dict, params: int, name: str, errors: dict) -> None:
	"""Writes a required text value of the query.

	Args:
		query: The values of the request, the value is written by its name.
		params: The query of the request (http_request_get_query_params ()).
		name: The key.
		errors: The errors of the request, "required" when it is missing, "invalid" when it is not utf-8.
	"""
	query_cast (query, params, name, str, errors, True)

def percepthor_query_value_from_params_with_cast (
	query: dict, params: int, name: str, cast: Callable [[str], Any], errors: dict
) -> None:
	"""Writes a required value of the query converted by a function.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		cast: Converts the text, raises an exception for an invalid one.
		errors: The errors of the request, "required" when it is missing, "invalid" when the cast fails.
	"""
	query_cast (query, params, name, cast, errors, True)

def percepthor_query_optional_value_from_params (
	query: dict, params: int, name: str, errors: dict | None = None
) -> None:
	"""Writes an optional text value of the query.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		errors: The errors of the request, "invalid" when the value is not utf-8; without them,
			a value that is not utf-8 is left out like a missing one.
	"""
	query_cast (query, params, name, str, errors, False)

def percepthor_query_optional_value_from_params_with_cast (
	query: dict, params: int, name: str, cast: Callable [[str], Any], errors: dict
) -> None:
	"""Writes an optional value of the query converted by a function.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		cast: Converts the text, raises an exception for an invalid one.
		errors: The errors of the request, "invalid" when the cast fails.
	"""
	query_cast (query, params, name, cast, errors, False)

def percepthor_query_int_value_from_params (query: dict, params: int, name: str, errors: dict) -> None:
	"""Writes a required integer value of the query.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		errors: The errors of the request, "required" when it is missing, "invalid" when it is not an integer.
	"""
	query_cast (query, params, name, int, errors, True)

def percepthor_query_int_optional_value_from_params (query: dict, params: int, name: str, errors: dict) -> None:
	"""Writes an optional integer value of the query.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		errors: The errors of the request, "invalid" when it is not an integer.
	"""
	query_cast (query, params, name, int, errors, False)

def percepthor_query_int_value_from_params_with_default (query: dict, params: int, name: str, default: int) -> None:
	"""Writes an integer value of the query, or a default when it is missing or invalid.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		default: The value when the query does not have a valid one.
	"""
	query_default (query, params, name, int, default)

def percepthor_query_float_value_from_params (query: dict, params: int, name: str, errors: dict) -> None:
	"""Writes a required number value of the query.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		errors: The errors of the request, "required" when it is missing, "invalid" when it is not a number.
	"""
	query_cast (query, params, name, float, errors, True)

def percepthor_query_float_optional_value_from_params (query: dict, params: int, name: str, errors: dict) -> None:
	"""Writes an optional number value of the query.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		errors: The errors of the request, "invalid" when it is not a number.
	"""
	query_cast (query, params, name, float, errors, False)

def percepthor_query_float_value_from_params_with_default (query: dict, params: int, name: str, default: float) -> None:
	"""Writes a number value of the query, or a default when it is missing or invalid.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		default: The value when the query does not have a valid one.
	"""
	query_default (query, params, name, float, default)

def percepthor_query_bool_value_from_params (query: dict, params: int, name: str, errors: dict) -> None:
	"""Writes a required truth value of the query ("true", "yes", "1", "false", "no", "0"...).

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		errors: The errors of the request, "required" when it is missing, "invalid" when it is not a truth value.
	"""
	query_cast (query, params, name, query_bool, errors, True)

def percepthor_query_bool_optional_value_from_params (query: dict, params: int, name: str, errors: dict) -> None:
	"""Writes an optional truth value of the query.

	Args:
		query: The values of the request.
		params: The query of the request.
		name: The key.
		errors: The errors of the request, "invalid" when it is not a truth value.
	"""
	query_cast (query, params, name, query_bool, errors, False)
