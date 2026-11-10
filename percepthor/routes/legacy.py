"""The routes of the first API of cerver authenticated by libauth.

Each function creates a route with ``http_route_create`` and its AuthRoute, to be registered
with ``http_cerver_route_register`` or added to another one with ``http_route_child_add``.
The handler is a Python function (http_receive, request) or an HttpHandler, kept for as long
as the process lives.
"""

from typing import Callable

from cerver.http import HTTP_ROUTE_AUTH_TYPE_CUSTOM
from cerver.http import http_handler, http_route_create, http_route_set_auth
from cerver.http import http_route_set_authentication_handler
from cerver.http import http_route_set_custom_data, http_route_set_delete_custom_data

from ..auth.handlers import percepthor_custom_authentication_handler
from ..auth.values import PERCEPTHOR_AUTH_SCOPE_SINGLE, PERCEPTHOR_AUTH_SCOPE_MANAGEMENT

from .routes import AUTH_ROUTE_DELETE_ROUTE
from .routes import auth_route_create, auth_route_create_action, auth_route_create_role
from .routes import auth_route_create_service, auth_route_create_permissions

__all__ = [
	"percepthor_route_auth_set", "percepthor_encode_optional", "percepthor_encode_required",
	"percepthor_route_create_internal", "percepthor_route_create", "percepthor_action_route_create",
	"percepthor_role_route_create", "percepthor_service_route_create",
	"percepthor_single_route_create", "percepthor_management_route_create"
]

TEXT_ENCODING = "utf-8"

def percepthor_route_auth_set (route: int, auth_route: int) -> None:
	"""Sets the AuthRoute of a route, released by cerver when the route is deleted.

	Args:
		route: The HttpRoute.
		auth_route: The AuthRoute.
	"""
	http_route_set_custom_data (route, auth_route)
	http_route_set_delete_custom_data (route, AUTH_ROUTE_DELETE_ROUTE)

def percepthor_encode_optional (value: str | None) -> bytes | None:
	"""Returns an optional value of a route as the bytes that libauth expects.

	Args:
		value: The value, None or "" for none.

	Returns:
		The bytes, None for a missing value.
	"""
	return value.encode (TEXT_ENCODING) if (value) else None

def percepthor_encode_required (value: str | None, name: str) -> bytes:
	"""Returns a required value of a route as the bytes that libauth expects.

	Args:
		value: The value.
		name: The name of the value, for the error.

	Returns:
		The bytes.

	Raises:
		ValueError: If the value is missing or empty.
	"""
	if (not value):
		raise ValueError (f"The {name} of the route is required")

	return value.encode (TEXT_ENCODING)

def percepthor_route_create_internal (method: int, path: str, handler: Callable) -> int:
	"""Creates a route authenticated by libauth, without its AuthRoute.

	Args:
		method: A REQUEST_METHOD_* value.
		path: The path of the route.
		handler: A Python function (http_receive, request) or an HttpHandler.

	Returns:
		The HttpRoute.
	"""
	percepthor_route = http_route_create (method, path.encode (TEXT_ENCODING), http_handler (handler))

	http_route_set_auth (percepthor_route, HTTP_ROUTE_AUTH_TYPE_CUSTOM)
	http_route_set_authentication_handler (percepthor_route, percepthor_custom_authentication_handler)

	return percepthor_route

def percepthor_route_create (method: int, path: str, handler: Callable) -> int:
	"""Creates a route that needs a valid token.

	Args:
		method: A REQUEST_METHOD_* value.
		path: The path of the route.
		handler: A Python function (http_receive, request) or an HttpHandler.

	Returns:
		The HttpRoute.
	"""
	percepthor_route = percepthor_route_create_internal (method, path, handler)

	percepthor_route_auth_set (percepthor_route, auth_route_create ())

	return percepthor_route

def percepthor_action_route_create (method: int, path: str, handler: Callable, action: str) -> int:
	"""Creates a route that needs an action of the role of the token.

	Args:
		method: A REQUEST_METHOD_* value.
		path: The path of the route.
		handler: A Python function (http_receive, request) or an HttpHandler.
		action: The action.

	Returns:
		The HttpRoute.

	Raises:
		ValueError: If the action is missing.
	"""
	action_route = percepthor_route_create_internal (method, path, handler)

	percepthor_route_auth_set (
		action_route, auth_route_create_action (percepthor_encode_required (action, "action"))
	)

	return action_route

def percepthor_role_route_create (method: int, path: str, handler: Callable, role: str, action: str) -> int:
	"""Creates a route that needs a role, and optionally an action.

	Args:
		method: A REQUEST_METHOD_* value.
		path: The path of the route.
		handler: A Python function (http_receive, request) or an HttpHandler.
		role: The role.
		action: The action, None or "" for any action.

	Returns:
		The HttpRoute.

	Raises:
		ValueError: If the role is missing.
	"""
	role_route = percepthor_route_create_internal (method, path, handler)

	percepthor_route_auth_set (
		role_route, auth_route_create_role (
			percepthor_encode_optional (action), percepthor_encode_required (role, "role")
		)
	)

	return role_route

def percepthor_service_route_create (method: int, path: str, handler: Callable) -> int:
	"""Creates a route that only accepts the token of a service.

	Args:
		method: A REQUEST_METHOD_* value.
		path: The path of the route.
		handler: A Python function (http_receive, request) or an HttpHandler.

	Returns:
		The HttpRoute.
	"""
	service_route = percepthor_route_create_internal (method, path, handler)

	percepthor_route_auth_set (service_route, auth_route_create_service ())

	return service_route

def percepthor_single_route_create (
	method: int, path: str, handler: Callable, permissions: int, action: str
) -> int:
	"""Creates a single permissions route.

	The route is not authenticated before its handler: the handler calls
	percepthor_single_authentication () with the resource of the request.

	Args:
		method: A REQUEST_METHOD_* value.
		path: The path of the route.
		handler: A Python function (http_receive, request) or an HttpHandler.
		permissions: A PERMISSIONS_TYPE_* value.
		action: The action over the resource.

	Returns:
		The HttpRoute.
	"""
	single_route = http_route_create (method, path.encode (TEXT_ENCODING), http_handler (handler))

	percepthor_route_auth_set (
		single_route,
		auth_route_create_permissions (
			PERCEPTHOR_AUTH_SCOPE_SINGLE, permissions,
			percepthor_encode_optional (action)
		)
	)

	return single_route

def percepthor_management_route_create (
	method: int, path: str, handler: Callable, permissions: int, action: str
) -> int:
	"""Creates a management permissions route, that gets every resource of a type.

	Args:
		method: A REQUEST_METHOD_* value.
		path: The path of the route.
		handler: A Python function (http_receive, request) or an HttpHandler.
		permissions: A PERMISSIONS_TYPE_* value.
		action: The action over the resources.

	Returns:
		The HttpRoute.
	"""
	management_route = percepthor_route_create_internal (method, path, handler)

	percepthor_route_auth_set (
		management_route,
		auth_route_create_permissions (
			PERCEPTHOR_AUTH_SCOPE_MANAGEMENT, permissions,
			percepthor_encode_optional (action)
		)
	)

	return management_route
