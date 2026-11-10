"""The loading of libauth and the conversions of its strings.

Bugs these tests fixed:
- libauth was always loaded from /usr/local/lib/libauth.so, a missing library raised a bare OSError
"""

import pytest

from percepthor import lib

pytestmark = [pytest.mark.unit]

class TestLibrary:

	def test_configured_path_goes_first (self, monkeypatch):
		monkeypatch.setenv (lib.AUTH_LIBRARY_VARIABLE, "/opt/custom/libauth.so")

		candidates = lib.auth_candidates ()

		assert candidates[0] == "/opt/custom/libauth.so"
		assert lib.AUTH_LIBRARY_DEFAULT_PATH in candidates

	def test_without_configuration (self, monkeypatch):
		monkeypatch.delenv (lib.AUTH_LIBRARY_VARIABLE, raising=False)

		assert lib.auth_candidates ()[0] == lib.AUTH_LIBRARY_DEFAULT_PATH

	def test_a_missing_library_names_the_variable (self, monkeypatch):
		monkeypatch.setattr (lib, "auth_candidates", lambda: ["/opt/missing/libauth.so"])

		with pytest.raises (lib.AuthLibraryError, match=lib.AUTH_LIBRARY_VARIABLE):
			lib.auth_load ()

	def test_the_error_is_an_import_error (self):
		assert issubclass (lib.AuthLibraryError, ImportError)

	def test_c_string (self):
		assert lib.auth_c_string ("ñ") == "ñ".encode ("utf-8")
		assert lib.auth_c_string (b"x") == b"x"
		assert lib.auth_c_string (None) is None

	def test_text (self):
		assert lib.auth_text (b"abc") == "abc"
		assert lib.auth_text (b"\xff") is None
		assert lib.auth_text (None) is None

	def test_every_function_is_registered (self):
		assert "percepthor_custom_authentication_handler" in lib.auth_functions
		assert lib.auth_functions["auth_route_create"].__doc__
