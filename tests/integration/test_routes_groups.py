"""The routes of percepthor in the tree that cerver compiles.

A real web cerver is created and its tree compiled, never started, like the
test_api_routes.py of the services: the groups, their roots, the subgroups, the auth
of every kind of endpoint and the registration errors are read from the tree.

Bugs these tests fixed:
- percepthor_group_create () returned the NULL of a group that cerver did not create,
  and the routes added to it failed later without a reason
- an auth setting replaced the authentication of percepthor
"""

import pytest

from cerver import cerver_create_web
from cerver import cerver_teardown
from cerver.http import HTTP_ROUTE_AUTH_TYPE_CUSTOM
from cerver.http import HTTP_ROUTE_AUTH_TYPE_NONE
from cerver.http import HTTP_ROUTE_MODIFIER_MULTI_PART
from cerver.http import REQUEST_METHOD_DELETE
from cerver.http import REQUEST_METHOD_GET
from cerver.http import REQUEST_METHOD_POST
from cerver.http import REQUEST_METHOD_PUT
from cerver.http import http_cerver_get
from cerver.http import http_cerver_routes_compile
from cerver.http import http_cerver_routes_errors_count
from cerver.http import http_cerver_routes_json
from cerver.http import http_endpoint_get_path
from cerver.http import http_route_auth_type_to_string
from cerver.http import http_route_modifier_to_string

from percepthor import PERMISSIONS_TYPE_ORGANIZATION
from percepthor import PERMISSIONS_TYPE_PROJECT
from percepthor import percepthor_group_create
from percepthor import percepthor_route
from percepthor import percepthor_subgroup_create
from percepthor.routes import PercepthorGroup
from percepthor.routes import percepthor_group_route
from percepthor.routes import percepthor_group_configure

pytestmark = [pytest.mark.integration]

CERVER_NAME = b"pypercepthor-routes-test"
CERVER_PORT = 5998
CERVER_CONNECTION_QUEUE = 4

TREE_ERRORS_NONE = 0

AUTH_CUSTOM = http_route_auth_type_to_string (HTTP_ROUTE_AUTH_TYPE_CUSTOM).decode ("utf-8")
AUTH_NONE = http_route_auth_type_to_string (HTTP_ROUTE_AUTH_TYPE_NONE).decode ("utf-8")

MODIFIER_MULTI_PART = http_route_modifier_to_string (HTTP_ROUTE_MODIFIER_MULTI_PART).decode ("utf-8")

def _handler (http_receive, request):
	return None

def _tree (http_cerver) -> dict:
	"""(method, path) -> endpoint of the compiled tree."""
	tree = http_cerver_routes_json (http_cerver)

	return {(endpoint["method"], endpoint["path"]): endpoint for endpoint in tree["endpoints"]}

@pytest.fixture
def http_cerver ():
	cerver = cerver_create_web (CERVER_NAME, CERVER_PORT, CERVER_CONNECTION_QUEUE)

	yield http_cerver_get (cerver)

	cerver_teardown (cerver)

def _register (http_cerver):
	"""The routes of a service with every kind of authentication."""
	api = percepthor_group_create (http_cerver, "api/test", REQUEST_METHOD_GET, _handler)

	percepthor_route (api, REQUEST_METHOD_GET, "token", _handler)
	percepthor_route (api, REQUEST_METHOD_POST, "action", _handler, action="test.create")
	percepthor_route (api, REQUEST_METHOD_POST, "role", _handler, role="admin")
	percepthor_route (api, REQUEST_METHOD_GET, "service", _handler, service=True)
	percepthor_route (api, REQUEST_METHOD_GET, "management", _handler, management=PERMISSIONS_TYPE_PROJECT)
	percepthor_route (api, REQUEST_METHOD_GET, "single/:id", _handler, single=PERMISSIONS_TYPE_ORGANIZATION, action="read")
	percepthor_route (api, REQUEST_METHOD_PUT, "internal", _handler, public=True)
	percepthor_route (api, REQUEST_METHOD_POST, "upload", _handler, modifier=HTTP_ROUTE_MODIFIER_MULTI_PART)

	items = percepthor_subgroup_create (api, "items", REQUEST_METHOD_GET, _handler)
	percepthor_route (items, REQUEST_METHOD_DELETE, ":id/delete", _handler)

	return api

EXPECTED_AUTH = {
	("GET", "/api/test"): AUTH_CUSTOM,
	("GET", "/api/test/token"): AUTH_CUSTOM,
	("POST", "/api/test/action"): AUTH_CUSTOM,
	("POST", "/api/test/role"): AUTH_CUSTOM,
	("GET", "/api/test/service"): AUTH_CUSTOM,
	("GET", "/api/test/management"): AUTH_CUSTOM,
	# a single endpoint authenticates itself, with the resource of its path
	("GET", "/api/test/single/:id"): AUTH_NONE,
	("PUT", "/api/test/internal"): AUTH_NONE,
	("POST", "/api/test/upload"): AUTH_CUSTOM,
	("GET", "/api/test/items"): AUTH_CUSTOM,
	("DELETE", "/api/test/items/:id/delete"): AUTH_CUSTOM
}

class TestGroupsTree:

	def test_tree_compiles (self, http_cerver):
		_register (http_cerver)

		assert http_cerver_routes_compile (http_cerver) == TREE_ERRORS_NONE
		assert http_cerver_routes_errors_count (http_cerver) == TREE_ERRORS_NONE

	def test_paths_are_the_registered (self, http_cerver):
		_register (http_cerver)
		http_cerver_routes_compile (http_cerver)

		assert set (_tree (http_cerver)) == set (EXPECTED_AUTH)

	@pytest.mark.parametrize ("method, path", list (EXPECTED_AUTH))
	def test_auth_of_every_endpoint (self, http_cerver, method, path):
		_register (http_cerver)
		http_cerver_routes_compile (http_cerver)

		assert _tree (http_cerver)[(method, path)]["auth"] == EXPECTED_AUTH[(method, path)]

	def test_modifier (self, http_cerver):
		_register (http_cerver)
		http_cerver_routes_compile (http_cerver)

		assert _tree (http_cerver)[("POST", "/api/test/upload")]["modifier"] == MODIFIER_MULTI_PART

	def test_group_without_authentication (self, http_cerver):
		public = percepthor_group_create (http_cerver, "api/public", authenticated=False)
		percepthor_route (public, REQUEST_METHOD_GET, "health", _handler, public=True)
		http_cerver_routes_compile (http_cerver)

		assert _tree (http_cerver)[("GET", "/api/public/health")]["auth"] == AUTH_NONE

class TestGroupsErrors:

	def test_duplicated_route_is_a_registration_error (self, http_cerver):
		api = percepthor_group_create (http_cerver, "api/test")
		percepthor_route (api, REQUEST_METHOD_GET, "token", _handler)
		percepthor_route (api, REQUEST_METHOD_GET, "token", _handler)

		assert http_cerver_routes_compile (http_cerver) != TREE_ERRORS_NONE

	def test_root_needs_its_method_and_its_handler (self, http_cerver):
		with pytest.raises (ValueError):
			percepthor_group_create (http_cerver, "api/test", REQUEST_METHOD_GET)

		with pytest.raises (ValueError):
			percepthor_group_create (http_cerver, "api/other", handler=_handler)

	def test_group_that_cerver_did_not_create_raises (self):
		with pytest.raises (ValueError):
			percepthor_group_create (None, "api/test")

	def test_subgroup_that_cerver_did_not_create_raises (self):
		with pytest.raises (ValueError):
			percepthor_subgroup_create (None, "items")

	def test_auth_setting_is_rejected (self, http_cerver):
		api = percepthor_group_create (http_cerver, "api/test")

		with pytest.raises (ValueError):
			percepthor_route (api, REQUEST_METHOD_GET, "token", _handler, auth=HTTP_ROUTE_AUTH_TYPE_NONE)

		with pytest.raises (ValueError):
			percepthor_group_route (api, REQUEST_METHOD_GET, _handler, auth=HTTP_ROUTE_AUTH_TYPE_NONE)

class TestPercepthorGroup:

	def test_decorators_and_subgroups (self, http_cerver):
		api = PercepthorGroup.create (http_cerver, "api/decorated")

		@api.post ("items/:id/delete", action="items.delete")
		def item_delete_handler (http_receive, request):
			return None

		items = api.subgroup ("items", REQUEST_METHOD_GET, _handler)
		endpoint = items.add (REQUEST_METHOD_GET, ":id", _handler)

		assert http_endpoint_get_path (endpoint).contents.str == b"/api/decorated/items/:id"

		http_cerver_routes_compile (http_cerver)
		tree = _tree (http_cerver)

		assert tree[("POST", "/api/decorated/items/:id/delete")]["auth"] == AUTH_CUSTOM
		assert tree[("GET", "/api/decorated/items")]["auth"] == AUTH_CUSTOM

	def test_create_without_cerver_raises (self):
		with pytest.raises (ValueError):
			PercepthorGroup.create (None, "api/test")

class TestGroupsSettings:

	def test_group_settings_are_inherited (self, http_cerver):
		api = percepthor_group_create (http_cerver, "api/settings")
		percepthor_group_configure (api, cors=True, etag=True, compression=True)

		percepthor_route (api, REQUEST_METHOD_GET, "items", _handler)
		percepthor_route (api, REQUEST_METHOD_GET, "plain", _handler, etag=False, compression=False)

		items = percepthor_subgroup_create (api, "items")
		percepthor_route (items, REQUEST_METHOD_GET, ":id", _handler)

		http_cerver_routes_compile (http_cerver)
		tree = _tree (http_cerver)

		for path in ("/api/settings/items", "/api/settings/items/:id"):
			endpoint = tree[("GET", path)]
			assert (endpoint["cors"], endpoint["etag"], endpoint["compression"]) == (True, True, True)

		plain = tree[("GET", "/api/settings/plain")]
		assert (plain["cors"], plain["etag"], plain["compression"]) == (True, False, False)

	def test_settings_without_values_are_not_set (self, http_cerver):
		api = percepthor_group_create (http_cerver, "api/defaults")
		percepthor_group_configure (api)
		percepthor_route (api, REQUEST_METHOD_GET, "items", _handler)

		http_cerver_routes_compile (http_cerver)
		endpoint = _tree (http_cerver)[("GET", "/api/defaults/items")]

		assert (endpoint["cors"], endpoint["etag"], endpoint["compression"]) == (False, False, False)

	def test_percepthor_group_configure_returns_the_group (self, http_cerver):
		api = PercepthorGroup.create (http_cerver, "api/decorated").configure (etag=True)

		@api.get ("items", compression=True)
		def items_handler (http_receive, request):
			return None

		http_cerver_routes_compile (http_cerver)
		endpoint = _tree (http_cerver)[("GET", "/api/decorated/items")]

		assert (endpoint["etag"], endpoint["compression"]) == (True, True)
