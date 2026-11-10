"""The AuthRoute of libauth: what a route requires from the token of its requests.

An AuthRoute is the custom data of a route, a group or an endpoint of cerver, and cerver
releases it with ``auth_route_delete`` when the route is deleted.
"""

from ctypes import c_void_p, c_char_p, cast

from cerver.http import RouteDeleteCustom

from ..lib import auth_function

from ..auth.permissions import PermissionsType
from ..auth.values import PercepthorAuthScope

__all__ = [
	"auth_route_delete", "auth_route_create", "auth_route_create_action", "auth_route_create_role",
	"auth_route_create_service", "auth_route_create_permissions", "auth_route_print",
	"AUTH_ROUTE_DELETE", "AUTH_ROUTE_DELETE_ROUTE"
]

auth_route_delete = auth_function (
	"auth_route_delete", [c_void_p], None,
	"""Releases an AuthRoute, the delete of the custom data of a route.

	Args:
		auth_route: The AuthRoute, None does nothing.
	"""
)

auth_route_create = auth_function (
	"auth_route_create", [], c_void_p,
	"""Creates the AuthRoute of a route that only needs a valid token.

	Returns:
		The AuthRoute, None on error.
	"""
)

auth_route_create_action = auth_function (
	"auth_route_create_action", [c_char_p], c_void_p,
	"""Creates the AuthRoute of a route that needs an action of the role of the token.

	Args:
		action: The action, as bytes.

	Returns:
		The AuthRoute, None on error.
	"""
)

auth_route_create_role = auth_function (
	"auth_route_create_role", [c_char_p, c_char_p], c_void_p,
	"""Creates the AuthRoute of a route that needs a role, and optionally an action.

	Args:
		action: The action as bytes, None for any action.
		role: The role, as bytes.

	Returns:
		The AuthRoute, None on error.
	"""
)

auth_route_create_service = auth_function (
	"auth_route_create_service", [], c_void_p,
	"""Creates the AuthRoute of a route that only accepts the token of a service.

	Returns:
		The AuthRoute, None on error.
	"""
)

auth_route_create_permissions = auth_function (
	"auth_route_create_permissions", [PercepthorAuthScope, PermissionsType, c_char_p], c_void_p,
	"""Creates the AuthRoute of a permissions route.

	Args:
		scope: PERCEPTHOR_AUTH_SCOPE_SINGLE or PERCEPTHOR_AUTH_SCOPE_MANAGEMENT.
		permissions_type: A PERMISSIONS_TYPE_* value.
		permissions_action: The action that the route needs as bytes, can be None.

	Returns:
		The AuthRoute, None on error.
	"""
)

auth_route_print = auth_function (
	"auth_route_print", [c_void_p], None,
	"""Prints the values of an AuthRoute.

	Args:
		auth_route: The AuthRoute, None does nothing.
	"""
)

# the C address of auth_route_delete (), so cerver releases the AuthRoute of a group
# or an endpoint at its teardown without calling back into python
AUTH_ROUTE_DELETE = cast (auth_route_delete, c_void_p)

# the same C function in the typed slot of a route of the first API, it wraps the C address
# and is not a python callback; the route releases its AuthRoute once, when cerver deletes it,
# the endpoint that translates it only borrows the pointer
AUTH_ROUTE_DELETE_ROUTE = cast (auth_route_delete, RouteDeleteCustom)
