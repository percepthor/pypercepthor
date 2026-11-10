"""Every module of the package imports over the real libcerver and libauth.

ctypes resolves every bound symbol when its module is imported, so a symbol that
libauth or libcerver does not export fails here instead of at the start of a service.
"""

import importlib
import pytest

pytestmark = [pytest.mark.unit]

PACKAGE_MODULES = (
	"percepthor",
	"percepthor.lib",
	"percepthor.version",
	"percepthor.auth",
	"percepthor.auth.handlers",
	"percepthor.auth.permissions",
	"percepthor.auth.services",
	"percepthor.auth.tokens",
	"percepthor.auth.values",
	"percepthor.routes",
	"percepthor.routes.admin",
	"percepthor.routes.groups",
	"percepthor.routes.legacy",
	"percepthor.routes.routes",
	"percepthor.validations",
	"percepthor.validations.bodies",
	"percepthor.validations.queries"
)

PACKAGE_ROOT = "/home/pypercepthor/percepthor"

class TestImports:

	@pytest.mark.parametrize ("module_name", PACKAGE_MODULES)
	def test_module_imports (self, module_name):
		assert importlib.import_module (module_name) is not None

	def test_the_package_is_the_working_tree (self):
		module = importlib.import_module ("percepthor")

		assert module.__file__.startswith (PACKAGE_ROOT)
