"""The admin routes of an HTTP cerver (/cerver/...) authenticated by libauth."""

from cerver.http import HTTP_ROUTE_AUTH_TYPE_CUSTOM
from cerver.http import http_cerver_enable_admin_routes
from cerver.http import http_cerver_enable_admin_routes_authentication
from cerver.http import http_cerver_admin_routes_set_authentication_handler
from cerver.http import http_cerver_admin_routes_set_custom_data
from cerver.http import http_cerver_admin_routes_set_delete_custom_data

from ..auth.handlers import percepthor_custom_authentication_handler

from .routes import AUTH_ROUTE_DELETE, auth_route_create

__all__ = [
	"percepthor_admin_routes_configuration"
]

def percepthor_admin_routes_configuration (http_cerver: int) -> None:
	"""Enables the admin routes of an HTTP cerver, authenticated with a token.

	Their AuthRoute is released by cerver at its teardown.

	Args:
		http_cerver: The HttpCerver.
	"""
	http_cerver_enable_admin_routes (http_cerver, True)
	http_cerver_enable_admin_routes_authentication (http_cerver, HTTP_ROUTE_AUTH_TYPE_CUSTOM)
	http_cerver_admin_routes_set_custom_data (http_cerver, auth_route_create ())
	http_cerver_admin_routes_set_delete_custom_data (http_cerver, AUTH_ROUTE_DELETE)
	http_cerver_admin_routes_set_authentication_handler (
		http_cerver, percepthor_custom_authentication_handler
	)
