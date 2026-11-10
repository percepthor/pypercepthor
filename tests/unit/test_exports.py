"""The names that the package exports: every module has its __all__, every name of it
exists, and the package does not leak what its modules import.

Bugs these tests fixed:
- `from percepthor import *` exported lib, json, ctypes and the names of cerver.http that
  the modules imported
"""

import importlib
import pkgutil

import pytest

import percepthor

pytestmark = [pytest.mark.unit]

MODULES = sorted (
	info.name for info in pkgutil.walk_packages (percepthor.__path__, "percepthor.")
)

# names that the package must never export, they belong to other packages
LEAKS = ("lib", "json", "ctypes", "c_void_p", "cast", "http_route_create", "http_handler", "HttpGroup", "strtobool")

class TestExports:

	@pytest.mark.parametrize ("module_name", MODULES)
	def test_module_has_its_all (self, module_name):
		module = importlib.import_module (module_name)

		assert isinstance (module.__all__, (list, tuple)), module_name
		assert len (module.__all__) == len (set (module.__all__)), module_name

		for name in module.__all__:
			assert hasattr (module, name), f"{module_name}.{name}"

	def test_package_exports_every_name_once (self):
		assert len (percepthor.__all__) == len (set (percepthor.__all__))

		for name in percepthor.__all__:
			assert hasattr (percepthor, name), name

	@pytest.mark.parametrize ("name", LEAKS)
	def test_package_does_not_leak (self, name):
		namespace = dict ()
		exec ("from percepthor import *", namespace)

		assert name not in namespace

	def test_version (self):
		assert percepthor.__version__ == percepthor.PERCEPTHOR_VERSION
		assert percepthor.version["libauth"] == percepthor.PERCEPTHOR_LIBAUTH_VERSION

	def test_token_types (self):
		assert percepthor.percepthor_token_type_to_string (percepthor.PERCEPTHOR_TOKEN_TYPE_USER) == b"User"
		assert percepthor.percepthor_token_type_to_string (64) == b"None"
