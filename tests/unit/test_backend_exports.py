"""Every symbol that a service or a worker imports from `percepthor` exists.

The list is the one of `from percepthor import X` across the backend repositories
(2026-11-06). A symbol renamed or removed from the package breaks every service that
imports it at its start, so it fails here first. Add the new ones when the backend
starts importing them.
"""

import pytest

import percepthor

pytestmark = [pytest.mark.unit]

BACKEND_SYMBOLS = (
	"PERCEPTHOR_AUTH_SCOPE_MANAGEMENT",
	"PERCEPTHOR_AUTH_SCOPE_NONE",
	"PERCEPTHOR_AUTH_SCOPE_SINGLE",
	"PERCEPTHOR_AUTH_TYPE_ACTION",
	"PERCEPTHOR_AUTH_TYPE_COMPLETE",
	"PERCEPTHOR_AUTH_TYPE_MULTIPLE",
	"PERCEPTHOR_AUTH_TYPE_NONE",
	"PERCEPTHOR_AUTH_TYPE_PERMISSIONS",
	"PERCEPTHOR_AUTH_TYPE_ROLE",
	"PERCEPTHOR_AUTH_TYPE_SERVICE",
	"PERCEPTHOR_AUTH_TYPE_TOKEN",
	"PERMISSIONS_TYPE_ORGANIZATION",
	"PERMISSIONS_TYPE_PROJECT",
	"auth_route_create",
	"auth_route_delete",
	"auth_service_create",
	"auth_service_delete",
	"percepthor_action_route_create",
	"percepthor_auth_get_admin",
	"percepthor_auth_get_token_id",
	"percepthor_auth_get_token_organization",
	"percepthor_auth_get_token_role",
	"percepthor_auth_get_token_user",
	"percepthor_auth_get_token_username",
	"percepthor_auth_permissions_iter_get_next",
	"percepthor_auth_permissions_iter_start",
	"percepthor_custom_authentication_handler",
	"percepthor_endpoint_authenticate",
	"percepthor_group_create",
	"percepthor_handle_body_input",
	"percepthor_libauth_version_print_full",
	"percepthor_management_route_create",
	"percepthor_route",
	"percepthor_route_create",
	"percepthor_single_authentication",
	"percepthor_single_route_create",
	"percepthor_subgroup_create",
	"permissions_get_resource",
	"permissions_print",
	"pypercepthor_version_print_full"
)

class TestBackendExports:

	@pytest.mark.parametrize ("symbol", BACKEND_SYMBOLS)
	def test_symbol_is_exported (self, symbol):
		assert hasattr (percepthor, symbol)
