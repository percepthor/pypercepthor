"""Every kind of route of percepthor authenticated by libauth against a real auth-service.

Each test mints its JWT with the key of the session, writes the keys of Redis that the
other services write in production, and calls the route of the cerver of percepthor.
libauth sends the token to auth-service and, when it accepts it, the handler answers the
values of the PercepthorAuth it received.

Bugs these tests fixed:
- auth-service answered 400, not 401, to a token that was revoked or not in Redis
- a role route without an action always failed: libauth sent "action": "" and
  auth-service required it, although it only checks it when it comes
- the mask of a user, an integer, crashed the cerver of the service: atoll (NULL)
- an API key never passed a service route: auth-service compared an ObjectId with a string
- the single authentication sent the empty action of the route instead of its
  permissions action, so it never passed
- a quote in the resource of a single authentication sent "scope": 0, which auth-service
  answers without checking any permission
- auth-service answered 200 to the types NONE, MULTIPLE and COMPLETE without checking anything
"""

import pytest
from bson import ObjectId

from percepthor import PERMISSIONS_TYPE_ORGANIZATION

from percepthor import PERCEPTHOR_AUTH_TYPE_COMPLETE
from percepthor import PERCEPTHOR_AUTH_TYPE_MULTIPLE
from percepthor import PERCEPTHOR_AUTH_TYPE_NONE
from percepthor import PERCEPTHOR_AUTH_TYPE_TOKEN

from e2e.conftest import ACTION_READ
from e2e.conftest import ROLE_NAME
from e2e.conftest import SERVICE_NAME
from e2e.conftest import SERVICE_REFERENCE
from e2e.conftest import TOKEN_PERMISSIONS_SCOPE_SERVICES
from e2e.conftest import TOKEN_STATUS_REVOKED
from e2e.conftest import e2e_auth_check
from e2e.conftest import e2e_get

pytestmark = [pytest.mark.e2e]

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401

AUTH_TYPE_NONE = PERCEPTHOR_AUTH_TYPE_NONE
AUTH_TYPE_TOKEN = PERCEPTHOR_AUTH_TYPE_TOKEN
AUTH_TYPE_MULTIPLE = PERCEPTHOR_AUTH_TYPE_MULTIPLE
AUTH_TYPE_COMPLETE = PERCEPTHOR_AUTH_TYPE_COMPLETE

SERVICE_MASK = 6

class TestToken:

	def test_without_token (self, identity):
		assert e2e_get ("/api/e2e/token").status == HTTP_UNAUTHORIZED

	def test_valid_token (self, identity):
		identity.token_data ()

		response = e2e_get ("/api/e2e/token", identity.jwt ())

		assert response.status == HTTP_OK
		assert response.body["token"] == identity.token
		assert response.body["organization"] == identity.organization
		assert response.body["user"] == identity.user
		assert response.body["role"] == identity.role

	def test_revoked_token (self, identity):
		identity.token_data (TOKEN_STATUS_REVOKED)

		assert e2e_get ("/api/e2e/token", identity.jwt ()).status == HTTP_UNAUTHORIZED

	def test_token_that_is_not_in_redis (self, identity):
		assert e2e_get ("/api/e2e/token", identity.jwt ()).status == HTTP_UNAUTHORIZED

	def test_token_signed_with_another_key (self, identity):
		identity.token_data ()

		assert e2e_get ("/api/e2e/token", identity.jwt ("other")).status == HTTP_UNAUTHORIZED

	def test_public_route_needs_no_token (self, identity):
		response = e2e_get ("/api/e2e/public")

		assert response.status == HTTP_OK
		assert response.body == {"public": "true"}

class TestAction:

	def test_role_with_the_action (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.role_actions (ACTION_READ)

		response = e2e_get ("/api/e2e/action", identity.jwt (), "POST")

		assert response.status == HTTP_OK
		assert response.body["token"] == identity.token

	def test_role_without_the_action (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.role_actions ("e2e.other")

		assert e2e_get ("/api/e2e/action", identity.jwt (), "POST").status == HTTP_UNAUTHORIZED

class TestRole:

	def test_role_without_action (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.role_name (ROLE_NAME)

		assert e2e_get ("/api/e2e/role", identity.jwt ()).status == HTTP_OK

	def test_another_role (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.role_name ("e2e-other-role")

		assert e2e_get ("/api/e2e/role", identity.jwt ()).status == HTTP_UNAUTHORIZED

	def test_role_with_its_action (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.role_name (ROLE_NAME)
		identity.role_actions (ACTION_READ)

		assert e2e_get ("/api/e2e/role/action", identity.jwt ()).status == HTTP_OK

	def test_role_without_its_action (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.role_name (ROLE_NAME)

		assert e2e_get ("/api/e2e/role/action", identity.jwt ()).status == HTTP_UNAUTHORIZED

class TestService:

	def test_user_mask_is_a_number (self, identity):
		identity.token_data ()
		identity.user_service_permissions (SERVICE_REFERENCE, SERVICE_MASK)

		response = e2e_get ("/api/e2e/service", identity.jwt ())

		assert response.status == HTTP_OK
		assert response.body["mask"] == SERVICE_MASK

	def test_organization_mask_is_a_string (self, identity):
		identity.token_data ()
		identity.organization_service_mask (SERVICE_REFERENCE, SERVICE_MASK)

		response = e2e_get ("/api/e2e/service", identity.jwt ())

		assert response.status == HTTP_OK
		assert response.body["mask"] == SERVICE_MASK

	def test_user_without_access (self, identity):
		identity.token_data ()

		assert e2e_get ("/api/e2e/service", identity.jwt ()).status == HTTP_UNAUTHORIZED

	def test_api_key_with_access (self, api_key):
		api_key.token_data ()
		api_key.token_permissions (
			TOKEN_PERMISSIONS_SCOPE_SERVICES,
			[{"service": ObjectId (SERVICE_REFERENCE), "actions_mask": SERVICE_MASK}]
		)

		response = e2e_get ("/api/e2e/service", api_key.jwt ())

		assert response.status == HTTP_OK
		assert response.body["mask"] == SERVICE_MASK

	def test_api_key_without_access (self, api_key):
		api_key.token_data ()
		api_key.token_permissions (
			TOKEN_PERMISSIONS_SCOPE_SERVICES,
			[{"service": ObjectId (), "actions_mask": SERVICE_MASK}]
		)

		assert e2e_get ("/api/e2e/service", api_key.jwt ()).status == HTTP_UNAUTHORIZED

class TestSingle:

	def test_resource_with_the_action (self, identity):
		resource = str (ObjectId ())

		identity.token_data ()
		identity.token_permissions ()
		identity.resource_actions (resource, PERMISSIONS_TYPE_ORGANIZATION, ACTION_READ)

		response = e2e_get (f"/api/e2e/single/{resource}", identity.jwt ())

		assert response.status == HTTP_OK
		assert response.body["resource"] == resource

	def test_resource_without_the_action (self, identity):
		resource = str (ObjectId ())

		identity.token_data ()
		identity.token_permissions ()
		identity.resource_actions (resource, PERMISSIONS_TYPE_ORGANIZATION, "e2e.other")

		assert e2e_get (f"/api/e2e/single/{resource}", identity.jwt ()).status == HTTP_UNAUTHORIZED

	def test_quotes_in_the_resource_do_not_change_the_scope (self, identity):
		identity.token_data ()
		identity.token_permissions ()

		response = e2e_get ("/api/e2e/single/x%22,%22scope%22:0,%22y%22:%22", identity.jwt ())

		assert response.status == HTTP_UNAUTHORIZED

	def test_admin_passes_every_resource (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.admin ()

		response = e2e_get (f"/api/e2e/single/{ObjectId ()}", identity.jwt ())

		assert response.status == HTTP_OK
		assert response.body["admin"] is True

class TestManagement:

	def test_resources_of_the_user (self, identity):
		first = str (ObjectId ())
		second = str (ObjectId ())

		identity.token_data ()
		identity.token_permissions ()
		identity.resource_actions (first, PERMISSIONS_TYPE_ORGANIZATION, ACTION_READ)
		identity.resource_actions (second, PERMISSIONS_TYPE_ORGANIZATION, ACTION_READ)

		response = e2e_get ("/api/e2e/management", identity.jwt ())

		assert response.status == HTTP_OK
		assert sorted (response.body["resources"]) == sorted ([first, second])
		assert response.body["admin"] is False

	def test_admin (self, identity):
		identity.token_data ()
		identity.token_permissions ()
		identity.admin ()

		response = e2e_get ("/api/e2e/management", identity.jwt ())

		assert response.status == HTTP_OK
		assert response.body["admin"] is True

	def test_token_without_the_actions_scope (self, identity):
		identity.token_data ()
		identity.token_permissions (TOKEN_PERMISSIONS_SCOPE_SERVICES)

		assert e2e_get ("/api/e2e/management", identity.jwt ()).status == HTTP_UNAUTHORIZED

class TestCheckTypes:
	"""The auth types of a direct call to /api/auth/check, public through nginx."""

	def test_token_type_passes (self, identity):
		identity.token_data ()

		assert e2e_auth_check ({"type": AUTH_TYPE_TOKEN, "source": SERVICE_NAME}, identity.jwt ()) == HTTP_OK

	@pytest.mark.parametrize ("auth_type", [AUTH_TYPE_NONE, AUTH_TYPE_MULTIPLE, AUTH_TYPE_COMPLETE])
	def test_types_without_a_check_are_rejected (self, identity, auth_type):
		identity.token_data ()

		assert e2e_auth_check ({"type": auth_type, "source": SERVICE_NAME}, identity.jwt ()) == HTTP_BAD_REQUEST
