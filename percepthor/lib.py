"""Loading of libauth and the declaration of its functions.

The library is loaded from the path in the ``AUTH_LIBRARY`` environment variable,
then from ``/usr/local/lib/libauth.so`` (where ``make install`` of libauth puts it),
and at last from the paths of the system linker.
"""

import ctypes
import ctypes.util
import os
from typing import Any

__all__ = [
	"AUTH_LIBRARY_VARIABLE", "AUTH_LIBRARY_DEFAULT_PATH", "AUTH_LIBRARY_NAME",
	"AuthLibraryError",
	"lib", "auth_functions", "auth_function"
]

AUTH_LIBRARY_VARIABLE = "AUTH_LIBRARY"
AUTH_LIBRARY_DEFAULT_PATH = "/usr/local/lib/libauth.so"
AUTH_LIBRARY_NAME = "auth"

class AuthLibraryError (ImportError):
	"""Raised when libauth can not be found or loaded."""

def auth_candidates () -> list:
	"""Returns the paths where libauth is looked for, in order."""
	candidates = []

	configured = os.environ.get (AUTH_LIBRARY_VARIABLE)
	if (configured):
		candidates.append (configured)

	candidates.append (AUTH_LIBRARY_DEFAULT_PATH)

	found = ctypes.util.find_library (AUTH_LIBRARY_NAME)
	if (found):
		candidates.append (found)

	return candidates

def auth_load () -> ctypes.CDLL:
	"""Loads libauth from the first path that works.

	Returns:
		The loaded library.

	Raises:
		AuthLibraryError: If no path has a library that can be loaded.
	"""
	errors = []

	library = None
	for candidate in auth_candidates ():
		try:
			library = ctypes.CDLL (candidate)
			break

		except OSError as error:
			errors.append (f"{candidate}: {error}")

	if (library is None):
		raise AuthLibraryError (
			"Failed to load libauth, install libauth or set "
			f"{AUTH_LIBRARY_VARIABLE} to its path ({'; '.join (errors)})"
		)

	return library

lib = auth_load ()

# every function that the package declares, by its name in libauth
auth_functions: dict = {}

def auth_function (name: str, argtypes: list, restype: Any, doc: str) -> Any:
	"""Declares a function of libauth with its types and its documentation.

	Args:
		name: The name of the function in libauth.
		argtypes: The ctypes of its arguments, [] for a function without them.
		restype: The ctypes of its result, None when it returns nothing.
		doc: Its docstring.

	Returns:
		The function of the library, ready to be called.
	"""
	function = getattr (lib, name)

	function.argtypes = argtypes
	function.restype = restype
	function.__doc__ = doc

	auth_functions[name] = function

	return function
