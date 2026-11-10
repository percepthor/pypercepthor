"""The types of the tokens that the auth service answers."""

from ctypes import c_char_p, c_int
from typing import TypeAlias

from ..lib import auth_function

__all__ = [
	"PercepthorTokenType",
	"PERCEPTHOR_TOKEN_TYPE_NONE", "PERCEPTHOR_TOKEN_TYPE_NORMAL", "PERCEPTHOR_TOKEN_TYPE_TEMPORARY",
	"PERCEPTHOR_TOKEN_TYPE_QUANTITY", "PERCEPTHOR_TOKEN_TYPE_USER",
	"percepthor_token_type_to_string"
]

PercepthorTokenType: TypeAlias = c_int # type: ignore

PERCEPTHOR_TOKEN_TYPE_NONE = 0
PERCEPTHOR_TOKEN_TYPE_NORMAL = 1
PERCEPTHOR_TOKEN_TYPE_TEMPORARY = 2
PERCEPTHOR_TOKEN_TYPE_QUANTITY = 3
PERCEPTHOR_TOKEN_TYPE_USER = 4

percepthor_token_type_to_string = auth_function (
	"percepthor_token_type_to_string", [PercepthorTokenType], c_char_p,
	"""Returns the name of a token type.

	Args:
		type: A PERCEPTHOR_TOKEN_TYPE_* value.

	Returns:
		The name as bytes, b"None" for an unknown type.
	"""
)
