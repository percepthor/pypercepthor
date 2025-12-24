"""Every binding of the package against the prototype of its function in the headers of libauth.

The headers are the ones installed in the image (/usr/local/include/auth), from the same
sources as libauth.so. Each binding has the number of arguments, the ctypes of each one and
of its result of its prototype, no binding is of an AUTH_PRIVATE function, and every public
function is bound or excluded with a reason.

Bugs these tests fixed:
- the functions without arguments did not declare argtypes = [], so ctypes accepted any
- the void functions did not declare restype = None, they returned a garbage int
- the version functions of libauth had neither argtypes nor restype
- auth_service_new and auth_service_delete were bound while they were AUTH_PRIVATE
"""

import ctypes
import re
from pathlib import Path

import pytest

from percepthor.lib import auth_functions

pytestmark = [pytest.mark.unit]

HEADERS = Path ("/usr/local/include/auth")

# the public functions that the package does not bind, with their reason
EXCLUDED = {
	"request_result_to_string": "the requests to the auth service are internal to libauth",
	"auth_request_authentication": "the requests to the auth service are internal to libauth",
	"percepthor_token_print": "it takes an AuthToken, that the package does not mirror (percepthor_auth_print_token prints it)"
}

ENUMS = ("PercepthorAuthType", "PercepthorAuthScope", "PermissionsType", "PercepthorTokenType", "RequestResult")

SCALARS = {
	"bool": ctypes.c_bool,
	"unsigned int": ctypes.c_uint,
	"int": ctypes.c_int,
	"int64_t": ctypes.c_int64
}

PROTOTYPE = re.compile (r"AUTH_(EXPORT|PUBLIC|PRIVATE)\s+([^;{]*?)\b(\w+)\s*\(([^)]*)\)\s*;", re.S)
COMMENTS = re.compile (r"/\*.*?\*/|//[^\n]*", re.S)

def c_type (declaration: str, result: bool):
	"""Returns the ctypes of a C type of a prototype, a parameter or a result."""
	text = re.sub (r"\bconst\b|\bstruct\b", " ", declaration)
	pointer = "*" in text
	text = " ".join (text.replace ("*", " ").split ())

	ctype = None
	if (pointer):
		ctype = ctypes.c_char_p if (text == "char") else ctypes.c_void_p

	elif (text in ENUMS):
		ctype = ctypes.c_int

	elif (text == "void"):
		ctype = None if (result) else ctypes.c_void_p

	else:
		ctype = SCALARS[text]

	return ctype

def parameter_type (parameter: str):
	"""Returns the ctypes of a parameter, without its name."""
	text = parameter.strip ()
	match = re.match (r"(.*?[\s*])(\w+)$", text)

	return c_type (match.group (1) if (match) else text, False)

def prototypes () -> dict:
	"""Returns every prototype of the headers, by its name: (visibility, result, parameters)."""
	found = dict ()

	for header in sorted (HEADERS.glob ("*.h")):
		text = COMMENTS.sub (" ", header.read_text ())
		for visibility, result, name, parameters in PROTOTYPE.findall (text):
			listed = [parameter for parameter in parameters.split (",") if (parameter.strip () not in ("", "void"))]
			found[name] = (
				visibility,
				c_type (result, True),
				[parameter_type (parameter) for parameter in listed]
			)

	return found

PROTOTYPES = prototypes ()

class TestBindings:

	def test_the_headers_were_read (self):
		assert len (PROTOTYPES) > len (auth_functions)

	@pytest.mark.parametrize ("name", sorted (auth_functions))
	def test_binding_matches_its_prototype (self, name):
		visibility, result, parameters = PROTOTYPES[name]
		function = auth_functions[name]

		assert visibility != "PRIVATE", f"{name} is AUTH_PRIVATE, libauth.so does not export it"
		assert list (function.argtypes) == parameters, name
		assert function.restype == result, name

	def test_every_public_function_is_bound_or_excluded (self):
		public = {name for name, (visibility, _, _) in PROTOTYPES.items () if (visibility != "PRIVATE")}

		assert public - set (auth_functions) - set (EXCLUDED) == set ()
		assert set (EXCLUDED) <= public
		assert not (set (EXCLUDED) & set (auth_functions))
