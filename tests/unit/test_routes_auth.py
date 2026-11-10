"""Unit tests for the auth values of percepthor.routes.groups.

percepthor_auth_route () picks the AuthRoute of an endpoint: single > management >
service > role > action > token. The creators of libauth are wrapped, so each case
sees which one was called and with which values.

Bugs these tests fixed:
- an action route without its action, or a role route without its role, raised
  AttributeError from None.encode (); now they raise a ValueError that names it
- the auth setting of an endpoint replaced the authentication that percepthor set
"""

import pytest
from unittest.mock import patch

from percepthor.routes import groups
from percepthor.routes import AUTH_ROUTE_DELETE
from percepthor.routes import auth_route_delete
from percepthor.routes import percepthor_auth_route
from percepthor.routes import percepthor_encode_optional
from percepthor.routes import percepthor_encode_required
from percepthor.routes import percepthor_endpoint_settings_check

from percepthor import PERCEPTHOR_AUTH_SCOPE_MANAGEMENT
from percepthor import PERCEPTHOR_AUTH_SCOPE_SINGLE
from percepthor import PERMISSIONS_TYPE_ORGANIZATION
from percepthor import PERMISSIONS_TYPE_PROJECT

pytestmark = [pytest.mark.unit]

ACTION = "tickets.create"
ROLE = "admin"

CREATORS = (
	"auth_route_create",
	"auth_route_create_action",
	"auth_route_create_role",
	"auth_route_create_service",
	"auth_route_create_permissions"
)

def _auth_route (**values):
	"""Runs percepthor_auth_route () with every creator of libauth wrapped, returns the one that was called."""
	called = dict ()

	def creator (name):
		def create (*args):
			called[name] = args
			return name

		return create

	patches = [patch.object (groups, name, side_effect=creator (name)) for name in CREATORS]
	for active in patches:
		active.start ()

	try:
		auth_route = percepthor_auth_route (**values)

	finally:
		for active in patches:
			active.stop ()

	return auth_route, called

class TestAuthRoutePrecedence:

	def test_token (self):
		auth_route, called = _auth_route ()
		assert called == {"auth_route_create": ()}

	def test_action (self):
		auth_route, called = _auth_route (action=ACTION)
		assert called == {"auth_route_create_action": (ACTION.encode ("utf-8"),)}

	def test_role_without_action (self):
		auth_route, called = _auth_route (role=ROLE)
		assert called == {"auth_route_create_role": (None, ROLE.encode ("utf-8"))}

	def test_role_over_action (self):
		auth_route, called = _auth_route (action=ACTION, role=ROLE)
		assert called == {"auth_route_create_role": (ACTION.encode ("utf-8"), ROLE.encode ("utf-8"))}

	def test_service_over_role (self):
		auth_route, called = _auth_route (action=ACTION, role=ROLE, service=True)
		assert called == {"auth_route_create_service": ()}

	def test_management_over_service (self):
		auth_route, called = _auth_route (action=ACTION, service=True, management=PERMISSIONS_TYPE_PROJECT)
		assert called == {
			"auth_route_create_permissions": (PERCEPTHOR_AUTH_SCOPE_MANAGEMENT, PERMISSIONS_TYPE_PROJECT, ACTION.encode ("utf-8"))
		}

	def test_single_over_management (self):
		auth_route, called = _auth_route (
			action=ACTION, management=PERMISSIONS_TYPE_PROJECT, single=PERMISSIONS_TYPE_ORGANIZATION
		)

		assert called == {
			"auth_route_create_permissions": (PERCEPTHOR_AUTH_SCOPE_SINGLE, PERMISSIONS_TYPE_ORGANIZATION, ACTION.encode ("utf-8"))
		}

	def test_management_without_action (self):
		auth_route, called = _auth_route (management=PERMISSIONS_TYPE_PROJECT)
		assert called == {
			"auth_route_create_permissions": (PERCEPTHOR_AUTH_SCOPE_MANAGEMENT, PERMISSIONS_TYPE_PROJECT, None)
		}

	def test_creates_a_real_auth_route (self):
		auth_route = percepthor_auth_route (action=ACTION)

		assert auth_route

		auth_route_delete (auth_route)

class TestEncode:

	def test_optional (self):
		assert percepthor_encode_optional (ACTION) == ACTION.encode ("utf-8")
		assert percepthor_encode_optional ("ñandú") == "ñandú".encode ("utf-8")
		assert percepthor_encode_optional (None) is None
		assert percepthor_encode_optional ("") is None

	def test_required (self):
		assert percepthor_encode_required (ROLE, "role") == ROLE.encode ("utf-8")

	@pytest.mark.parametrize ("value", [None, ""])
	def test_required_without_value_names_it (self, value):
		with pytest.raises (ValueError, match="role"):
			percepthor_encode_required (value, "role")

class TestEndpointSettings:

	def test_settings_without_auth (self):
		percepthor_endpoint_settings_check ({"modifier": 1, "max_body_size": 8})

	def test_auth_setting_is_rejected (self):
		with pytest.raises (ValueError):
			percepthor_endpoint_settings_check ({"auth": 0})

	def test_delete_is_the_address_of_libauth (self):
		assert AUTH_ROUTE_DELETE.value
