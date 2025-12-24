"""Unit tests for auth.py, permissions.py and service.py - the bindings of libauth.

The constants of the package are the enums of libauth: a constant that drifts from
its C value sends another auth type or scope to the auth service. The getters accept
the NULL custom data of a request that libauth did not authenticate.
"""

import pytest
import re
from pathlib import Path

from percepthor import PERCEPTHOR_AUTH_SCOPE_MANAGEMENT
from percepthor import PERCEPTHOR_AUTH_SCOPE_NONE
from percepthor import PERCEPTHOR_AUTH_SCOPE_SINGLE
from percepthor import PERCEPTHOR_AUTH_TYPE_ACTION
from percepthor import PERCEPTHOR_AUTH_TYPE_COMPLETE
from percepthor import PERCEPTHOR_AUTH_TYPE_MULTIPLE
from percepthor import PERCEPTHOR_AUTH_TYPE_NONE
from percepthor import PERCEPTHOR_AUTH_TYPE_PERMISSIONS
from percepthor import PERCEPTHOR_AUTH_TYPE_ROLE
from percepthor import PERCEPTHOR_AUTH_TYPE_SERVICE
from percepthor import PERCEPTHOR_AUTH_TYPE_TOKEN
from percepthor import PERMISSIONS_TYPE_NONE
from percepthor import PERMISSIONS_TYPE_ORGANIZATION
from percepthor import PERMISSIONS_TYPE_PROJECT
from percepthor import PERMISSIONS_TYPE_SERVICE
from percepthor import auth_service_create
from percepthor import auth_service_delete
from percepthor import auth_service_print
from percepthor import percepthor_auth_create
from percepthor import percepthor_auth_delete
from percepthor import percepthor_auth_get_action
from percepthor import percepthor_auth_get_admin
from percepthor import percepthor_auth_get_mask
from percepthor import percepthor_auth_get_permissions
from percepthor import percepthor_auth_get_resource
from percepthor import percepthor_auth_get_scope
from percepthor import percepthor_auth_get_token_id
from percepthor import percepthor_auth_get_token_organization
from percepthor import percepthor_auth_get_token_role
from percepthor import percepthor_auth_get_token_type
from percepthor import percepthor_auth_get_token_user
from percepthor import percepthor_auth_get_token_username
from percepthor import percepthor_auth_get_type
from percepthor import percepthor_auth_permissions_iter_get_next
from percepthor import percepthor_auth_permissions_iter_start
from percepthor import percepthor_auth_print_token
from percepthor import percepthor_auth_scope_to_string
from percepthor import percepthor_auth_type_to_string
from percepthor import permissions_get_resource
from percepthor import permissions_has_action
from percepthor import permissions_print
from percepthor import permissions_type_to_string

pytestmark = [pytest.mark.unit]

LIBAUTH_HEADERS = Path ("/usr/local/include/auth")

ENUM_ENTRY = re.compile (r"XX\((\d+),\s*(\w+),")

OUT_OF_RANGE = 64

AUTH_TYPES = {
	"NONE": PERCEPTHOR_AUTH_TYPE_NONE,
	"TOKEN": PERCEPTHOR_AUTH_TYPE_TOKEN,
	"ACTION": PERCEPTHOR_AUTH_TYPE_ACTION,
	"ROLE": PERCEPTHOR_AUTH_TYPE_ROLE,
	"SERVICE": PERCEPTHOR_AUTH_TYPE_SERVICE,
	"PERMISSIONS": PERCEPTHOR_AUTH_TYPE_PERMISSIONS,
	"MULTIPLE": PERCEPTHOR_AUTH_TYPE_MULTIPLE,
	"COMPLETE": PERCEPTHOR_AUTH_TYPE_COMPLETE
}

AUTH_SCOPES = {
	"NONE": PERCEPTHOR_AUTH_SCOPE_NONE,
	"SINGLE": PERCEPTHOR_AUTH_SCOPE_SINGLE,
	"MANAGEMENT": PERCEPTHOR_AUTH_SCOPE_MANAGEMENT
}

PERMISSIONS_TYPES = {
	"NONE": PERMISSIONS_TYPE_NONE,
	"SERVICE": PERMISSIONS_TYPE_SERVICE,
	"ORGANIZATION": PERMISSIONS_TYPE_ORGANIZATION,
	"PROJECT": PERMISSIONS_TYPE_PROJECT
}

def _header_enum (header: str, map_name: str) -> dict:
	"""The name -> value of an XX map of a header of libauth."""
	text = (LIBAUTH_HEADERS / header).read_text ()
	block = text.split (f"#define {map_name}(XX)")[1].split ("typedef")[0]

	return {name: int (value) for value, name in ENUM_ENTRY.findall (block)}

class TestConstants:

	def test_auth_types_are_the_ones_of_libauth (self):
		assert _header_enum ("auth.h", "PERCEPTHOR_AUTH_TYPE_MAP") == AUTH_TYPES

	def test_auth_scopes_are_the_ones_of_libauth (self):
		assert _header_enum ("auth.h", "PERCEPTHOR_AUTH_SCOPE_MAP") == AUTH_SCOPES

	def test_permissions_types_are_the_ones_of_libauth (self):
		assert _header_enum ("permissions.h", "PERMISSIONS_TYPE_MAP") == PERMISSIONS_TYPES

class TestToString:

	@pytest.mark.parametrize ("name, value", AUTH_TYPES.items ())
	def test_auth_type (self, name, value):
		assert percepthor_auth_type_to_string (value).decode ("utf-8").upper () == name

	@pytest.mark.parametrize ("name, value", AUTH_SCOPES.items ())
	def test_auth_scope (self, name, value):
		assert percepthor_auth_scope_to_string (value).decode ("utf-8").upper () == name

	@pytest.mark.parametrize ("name, value", PERMISSIONS_TYPES.items ())
	def test_permissions_type (self, name, value):
		assert permissions_type_to_string (value).decode ("utf-8").upper () == name

	def test_out_of_range_is_none (self):
		assert percepthor_auth_type_to_string (OUT_OF_RANGE) == b"None"
		assert percepthor_auth_scope_to_string (OUT_OF_RANGE) == b"None"
		assert permissions_type_to_string (OUT_OF_RANGE) == b"None"

class TestAuthValues:

	@pytest.mark.parametrize ("auth_type", AUTH_TYPES.values ())
	def test_created_auth_is_empty (self, auth_type):
		auth = percepthor_auth_create (auth_type)

		assert percepthor_auth_get_type (auth) == auth_type
		assert percepthor_auth_get_scope (auth) == PERCEPTHOR_AUTH_SCOPE_NONE
		assert percepthor_auth_get_token_id (auth) == b""
		assert percepthor_auth_get_token_user (auth) == b""
		assert percepthor_auth_get_admin (auth) is False
		assert percepthor_auth_get_mask (auth) == 0

		# only the permissions keep a list of resources
		assert bool (percepthor_auth_get_permissions (auth)) == (auth_type == PERCEPTHOR_AUTH_TYPE_PERMISSIONS)
		assert percepthor_auth_permissions_iter_start (auth) is False

		percepthor_auth_print_token (auth)
		percepthor_auth_delete (auth)

	def test_getters_accept_a_request_without_auth (self):
		assert percepthor_auth_get_type (None) == PERCEPTHOR_AUTH_TYPE_NONE
		assert percepthor_auth_get_scope (None) == PERCEPTHOR_AUTH_SCOPE_NONE
		assert percepthor_auth_get_resource (None) is None
		assert percepthor_auth_get_action (None) is None
		assert percepthor_auth_get_admin (None) is False
		assert percepthor_auth_get_permissions (None) is None
		assert percepthor_auth_permissions_iter_start (None) is False
		assert percepthor_auth_permissions_iter_get_next (None) is None
		assert percepthor_auth_get_token_id (None) is None
		assert percepthor_auth_get_token_type (None) == 0
		assert percepthor_auth_get_token_organization (None) is None
		assert percepthor_auth_get_token_role (None) is None
		assert percepthor_auth_get_token_user (None) is None
		assert percepthor_auth_get_token_username (None) is None
		assert percepthor_auth_get_mask (None) == 0

		percepthor_auth_print_token (None)
		percepthor_auth_delete (None)

class TestPermissions:

	def test_without_permissions (self):
		assert permissions_get_resource (None) is None
		assert permissions_has_action (None, b"read") is False

		permissions_print (None)

class TestAuthService:

	def test_create (self):
		service = auth_service_create (b"507f1f77bcf86cd799439011", b"tickets", b"http://auth:5020/api/auth/check")

		assert service

		auth_service_print (service)
		auth_service_delete (service)

	def test_create_without_an_id (self):
		service = auth_service_create (None, b"tickets", b"http://auth:5020/api/auth/check")

		assert service

		auth_service_print (service)
		auth_service_delete (service)

	def test_values_longer_than_their_fields_are_truncated (self):
		service = auth_service_create (b"i" * 512, b"n" * 512, b"a" * 512)

		assert service

		auth_service_delete (service)
		auth_service_print (None)
