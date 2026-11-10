"""The legacy routes of percepthor, registered in a real web cerver and compiled.

The percepthor_*_route_create () functions of the routes API that most services still
use: each one creates the route with its AuthRoute, and the tree compiles with them.

Bugs these tests fixed:
- an action route without its action, a role route without its role and a single route
  without its action raised AttributeError from None.encode ()
- the routes never released their AuthRoute: the delete of their custom data was commented out
- a plain Python handler was passed to http_route_create without being kept: ctypes rejects it
- the AuthRoute of the admin routes was never released, its delete was commented out
"""

import pytest
from ctypes import c_void_p
from ctypes import cast
from unittest.mock import patch

from cerver import cerver_create_web
from cerver import cerver_teardown
from cerver.http import REQUEST_METHOD_GET
from cerver.http import REQUEST_METHOD_POST
from cerver.http import http_cerver_get
from cerver.http import http_cerver_route_register
from cerver.http import http_cerver_routes_compile
from cerver.http import http_handler
from cerver.http import http_route_child_add

from percepthor import PERMISSIONS_TYPE_ORGANIZATION
from percepthor import PERMISSIONS_TYPE_PROJECT
from percepthor import percepthor_action_route_create
from percepthor import percepthor_management_route_create
from percepthor import percepthor_route_create
from percepthor import percepthor_single_route_create
from percepthor.routes import admin, legacy
from percepthor.routes import AUTH_ROUTE_DELETE
from percepthor.routes import percepthor_admin_routes_configuration
from percepthor.routes import percepthor_role_route_create
from percepthor.routes import percepthor_service_route_create

pytestmark = [pytest.mark.integration]

CERVER_NAME = b"pypercepthor-legacy-test"
CERVER_PORT = 5997
CERVER_CONNECTION_QUEUE = 4

TREE_ERRORS_NONE = 0

def _handler (http_receive, request):
	return None

HANDLER = http_handler (_handler)

@pytest.fixture
def http_cerver ():
	cerver = cerver_create_web (CERVER_NAME, CERVER_PORT, CERVER_CONNECTION_QUEUE)

	yield http_cerver_get (cerver)

	cerver_teardown (cerver)

class TestLegacyRoutes:

	def test_every_kind_of_route_compiles (self, http_cerver):
		main = percepthor_route_create (REQUEST_METHOD_GET, "api/legacy", HANDLER)

		children = (
			percepthor_route_create (REQUEST_METHOD_GET, "token", HANDLER),
			percepthor_action_route_create (REQUEST_METHOD_POST, "action", HANDLER, "legacy.create"),
			percepthor_role_route_create (REQUEST_METHOD_POST, "role", HANDLER, "admin", None),
			percepthor_role_route_create (REQUEST_METHOD_POST, "role/action", HANDLER, "admin", "legacy.create"),
			percepthor_service_route_create (REQUEST_METHOD_GET, "service", HANDLER),
			percepthor_management_route_create (REQUEST_METHOD_GET, "management", HANDLER, PERMISSIONS_TYPE_PROJECT, None),
			percepthor_single_route_create (REQUEST_METHOD_GET, "single/:id", HANDLER, PERMISSIONS_TYPE_ORGANIZATION, None)
		)

		for child in children:
			assert child
			http_route_child_add (main, child)

		http_cerver_route_register (http_cerver, main)
		percepthor_admin_routes_configuration (http_cerver)

		assert http_cerver_routes_compile (http_cerver) == TREE_ERRORS_NONE

	def test_every_kind_of_route_releases_its_auth_route (self, http_cerver):
		# the teardown of the fixture deletes the routes, and each one its AuthRoute once:
		# under ASan a double free of the endpoint that translates it would abort here
		with patch.object (legacy, "http_route_set_delete_custom_data", wraps=legacy.http_route_set_delete_custom_data) as spy:
			main = percepthor_route_create (REQUEST_METHOD_GET, "api/released", HANDLER)

			children = (
				percepthor_action_route_create (REQUEST_METHOD_POST, "action", HANDLER, "legacy.create"),
				percepthor_role_route_create (REQUEST_METHOD_POST, "role", HANDLER, "admin", None),
				percepthor_service_route_create (REQUEST_METHOD_GET, "service", HANDLER),
				percepthor_management_route_create (REQUEST_METHOD_GET, "management", HANDLER, PERMISSIONS_TYPE_PROJECT, None),
				percepthor_single_route_create (REQUEST_METHOD_GET, "single/:id", HANDLER, PERMISSIONS_TYPE_ORGANIZATION, None)
			)

		for child in children:
			http_route_child_add (main, child)

		http_cerver_route_register (http_cerver, main)

		assert http_cerver_routes_compile (http_cerver) == TREE_ERRORS_NONE

		released = {call.args[0] for call in spy.call_args_list if (cast (call.args[1], c_void_p).value == AUTH_ROUTE_DELETE.value)}

		assert released == {main, *children}

	def test_action_route_without_action_names_it (self):
		with pytest.raises (ValueError, match="action"):
			percepthor_action_route_create (REQUEST_METHOD_POST, "action", HANDLER, None)

	def test_role_route_without_role_names_it (self):
		with pytest.raises (ValueError, match="role"):
			percepthor_role_route_create (REQUEST_METHOD_POST, "role", HANDLER, None, "legacy.create")

	def test_plain_python_handler (self, http_cerver):
		main = percepthor_route_create (REQUEST_METHOD_GET, "api/plain", _handler)
		http_route_child_add (main, percepthor_single_route_create (
			REQUEST_METHOD_GET, "single/:id", _handler, PERMISSIONS_TYPE_ORGANIZATION, "plain.read"
		))

		http_cerver_route_register (http_cerver, main)

		assert http_cerver_routes_compile (http_cerver) == TREE_ERRORS_NONE

	def test_admin_routes_release_their_auth_route (self, http_cerver):
		with patch.object (admin, "http_cerver_admin_routes_set_delete_custom_data", wraps=admin.http_cerver_admin_routes_set_delete_custom_data) as spy:
			percepthor_admin_routes_configuration (http_cerver)

		spy.assert_called_once ()
		assert spy.call_args.args[1].value == AUTH_ROUTE_DELETE.value
