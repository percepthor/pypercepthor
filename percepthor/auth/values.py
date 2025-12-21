"""The values of an authenticated request: the PercepthorAuth that libauth keeps as the
custom data of the request (``http_request_get_custom_data (request)``).

Every getter accepts NULL (None or 0), the custom data of a request that libauth did not
authenticate, and returns its empty value.
"""

from ctypes import c_void_p, c_char_p, c_int, c_int64, c_bool
from typing import TypeAlias

from ..lib import auth_function

__all__ = [
	"PercepthorAuthType",
	"PERCEPTHOR_AUTH_TYPE_NONE", "PERCEPTHOR_AUTH_TYPE_TOKEN", "PERCEPTHOR_AUTH_TYPE_ACTION",
	"PERCEPTHOR_AUTH_TYPE_ROLE", "PERCEPTHOR_AUTH_TYPE_SERVICE", "PERCEPTHOR_AUTH_TYPE_PERMISSIONS",
	"PERCEPTHOR_AUTH_TYPE_MULTIPLE", "PERCEPTHOR_AUTH_TYPE_COMPLETE",
	"PercepthorAuthScope",
	"PERCEPTHOR_AUTH_SCOPE_NONE", "PERCEPTHOR_AUTH_SCOPE_SINGLE", "PERCEPTHOR_AUTH_SCOPE_MANAGEMENT",
	"percepthor_auth_type_to_string", "percepthor_auth_scope_to_string",
	"percepthor_auth_create", "percepthor_auth_delete",
	"percepthor_auth_get_type", "percepthor_auth_get_scope",
	"percepthor_auth_get_resource", "percepthor_auth_get_action",
	"percepthor_auth_get_admin", "percepthor_auth_get_permissions",
	"percepthor_auth_permissions_iter_start", "percepthor_auth_permissions_iter_get_next",
	"percepthor_auth_get_token_id", "percepthor_auth_get_token_type",
	"percepthor_auth_get_token_organization", "percepthor_auth_get_token_permissions",
	"percepthor_auth_get_token_role", "percepthor_auth_get_token_user",
	"percepthor_auth_get_token_username", "percepthor_auth_get_mask",
	"percepthor_auth_print_token"
]

PercepthorAuthType: TypeAlias = c_int # type: ignore

PERCEPTHOR_AUTH_TYPE_NONE = 0
PERCEPTHOR_AUTH_TYPE_TOKEN = 1
PERCEPTHOR_AUTH_TYPE_ACTION = 2
PERCEPTHOR_AUTH_TYPE_ROLE = 3
PERCEPTHOR_AUTH_TYPE_SERVICE = 4
PERCEPTHOR_AUTH_TYPE_PERMISSIONS = 5
# reserved by libauth, a route of these types is always rejected
PERCEPTHOR_AUTH_TYPE_MULTIPLE = 6
PERCEPTHOR_AUTH_TYPE_COMPLETE = 7

PercepthorAuthScope: TypeAlias = c_int # type: ignore

PERCEPTHOR_AUTH_SCOPE_NONE = 0
PERCEPTHOR_AUTH_SCOPE_SINGLE = 1
PERCEPTHOR_AUTH_SCOPE_MANAGEMENT = 2

percepthor_auth_type_to_string = auth_function (
	"percepthor_auth_type_to_string", [PercepthorAuthType], c_char_p,
	"""Returns the name of an auth type.

	Args:
		type: A PERCEPTHOR_AUTH_TYPE_* value.

	Returns:
		The name as bytes, b"None" for an unknown type.
	"""
)

percepthor_auth_scope_to_string = auth_function (
	"percepthor_auth_scope_to_string", [PercepthorAuthScope], c_char_p,
	"""Returns the name of an auth scope.

	Args:
		scope: A PERCEPTHOR_AUTH_SCOPE_* value.

	Returns:
		The name as bytes, b"None" for an unknown scope.
	"""
)

percepthor_auth_create = auth_function (
	"percepthor_auth_create", [PercepthorAuthType], c_void_p,
	"""Creates the auth values of a type, a permissions one with its list.

	Args:
		type: A PERCEPTHOR_AUTH_TYPE_* value.

	Returns:
		The PercepthorAuth, released with percepthor_auth_delete (), None on error.
	"""
)

percepthor_auth_delete = auth_function (
	"percepthor_auth_delete", [c_void_p], None,
	"""Releases a PercepthorAuth and its permissions.

	Args:
		auth: The PercepthorAuth, None does nothing.
	"""
)

percepthor_auth_get_type = auth_function (
	"percepthor_auth_get_type", [c_void_p], PercepthorAuthType,
	"""Returns the type of the route that authenticated the request.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		A PERCEPTHOR_AUTH_TYPE_* value, PERCEPTHOR_AUTH_TYPE_NONE for NULL.
	"""
)

percepthor_auth_get_scope = auth_function (
	"percepthor_auth_get_scope", [c_void_p], PercepthorAuthScope,
	"""Returns the scope of a permissions route.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		A PERCEPTHOR_AUTH_SCOPE_* value, PERCEPTHOR_AUTH_SCOPE_NONE for NULL.
	"""
)

percepthor_auth_get_resource = auth_function (
	"percepthor_auth_get_resource", [c_void_p], c_char_p,
	"""Returns the resource of a single permissions route.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The resource as bytes, None for NULL.
	"""
)

percepthor_auth_get_action = auth_function (
	"percepthor_auth_get_action", [c_void_p], c_char_p,
	"""Returns the action of a single permissions route.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The action as bytes, None for NULL.
	"""
)

percepthor_auth_get_admin = auth_function (
	"percepthor_auth_get_admin", [c_void_p], c_bool,
	"""Returns whether the auth service answered that the user is a super admin.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		True for an admin, False for NULL.
	"""
)

percepthor_auth_get_permissions = auth_function (
	"percepthor_auth_get_permissions", [c_void_p], c_void_p,
	"""Returns the list of the permissions of a management permissions route.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The DoubleList of Permissions, None for NULL or for any other route.
	"""
)

percepthor_auth_permissions_iter_start = auth_function (
	"percepthor_auth_permissions_iter_start", [c_void_p], c_bool,
	"""Starts the iteration of the permissions.

	The state of the iteration lives in the PercepthorAuth, so two threads can not
	iterate the same one at the same time.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		True when there are permissions to iterate.
	"""
)

percepthor_auth_permissions_iter_get_next = auth_function (
	"percepthor_auth_permissions_iter_get_next", [c_void_p], c_void_p,
	"""Returns the next permissions of the iteration.

	Args:
		auth: The PercepthorAuth, after percepthor_auth_permissions_iter_start ().

	Returns:
		The Permissions (see permissions_get_resource ()), None after the last one.
	"""
)

percepthor_auth_get_token_id = auth_function (
	"percepthor_auth_get_token_id", [c_void_p], c_char_p,
	"""Returns the id of the token.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The id as bytes, None for NULL.
	"""
)

percepthor_auth_get_token_type = auth_function (
	"percepthor_auth_get_token_type", [c_void_p], c_int,
	"""Returns the type of the token.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		A PERCEPTHOR_TOKEN_TYPE_* value, PERCEPTHOR_TOKEN_TYPE_NONE for NULL.
	"""
)

percepthor_auth_get_token_organization = auth_function (
	"percepthor_auth_get_token_organization", [c_void_p], c_char_p,
	"""Returns the organization of the token.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The organization as bytes, None for NULL.
	"""
)

percepthor_auth_get_token_permissions = auth_function (
	"percepthor_auth_get_token_permissions", [c_void_p], c_char_p,
	"""Returns the permissions of the token.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The permissions as bytes, None for NULL.
	"""
)

percepthor_auth_get_token_role = auth_function (
	"percepthor_auth_get_token_role", [c_void_p], c_char_p,
	"""Returns the role of the token.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The role as bytes, None for NULL.
	"""
)

percepthor_auth_get_token_user = auth_function (
	"percepthor_auth_get_token_user", [c_void_p], c_char_p,
	"""Returns the user of the token.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The user as bytes, None for NULL.
	"""
)

percepthor_auth_get_token_username = auth_function (
	"percepthor_auth_get_token_username", [c_void_p], c_char_p,
	"""Returns the username of the token.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The username as bytes, None for NULL.
	"""
)

percepthor_auth_get_mask = auth_function (
	"percepthor_auth_get_mask", [c_void_p], c_int64,
	"""Returns the actions mask that the auth service answered for a service route.

	Args:
		auth: The PercepthorAuth of the request.

	Returns:
		The mask, 0 for NULL.
	"""
)

percepthor_auth_print_token = auth_function (
	"percepthor_auth_print_token", [c_void_p], None,
	"""Prints the token of the auth values.

	Args:
		auth: The PercepthorAuth, None does nothing.
	"""
)
