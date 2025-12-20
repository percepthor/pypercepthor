"""Loading of libauth and the declaration of its functions.

The library is loaded from the path in the ``AUTH_LIBRARY`` environment variable,
then from ``/usr/local/lib/libauth.so`` (where ``make install`` of libauth puts it),
and at last from the paths of the system linker.
"""

import ctypes
import ctypes.util
import os

__all__ = [
	"AUTH_LIBRARY_VARIABLE", "AUTH_LIBRARY_DEFAULT_PATH", "AUTH_LIBRARY_NAME",
	"AuthLibraryError",
	"lib"
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
