"""The groups and endpoints of the routes tree of cerver authenticated by libauth.

A group created here authenticates its endpoints with a token, and each endpoint can require
its own action, role, service token or permissions:

	api = PercepthorGroup.create (http_cerver, "api/tickets")

	@api.post ("/:id/close", action="tickets.close")
	def ticket_close (http_receive, request):
		...

When several of them are given, the first one of single, management, service, role and
action is the one that is used.
"""

from typing import Callable

from cerver.http import HTTP_ROUTE_AUTH_TYPE_CUSTOM, HTTP_ROUTE_AUTH_TYPE_NONE
from cerver.http import HttpGroup, http_handler, http_endpoint_configure
from cerver.http import http_cerver_group_create, http_group_create, http_group_route_add
from cerver.http import http_group_root_add
from cerver.http import http_group_set_auth, http_group_set_authentication_handler
from cerver.http import http_group_set_custom_data
from cerver.http import http_group_set_cors, http_group_set_etag, http_group_set_compression
from cerver.http import http_endpoint_set_auth, http_endpoint_set_authentication_handler
from cerver.http import http_endpoint_set_custom_data

from ..auth.handlers import percepthor_custom_authentication_handler
from ..auth.values import PERCEPTHOR_AUTH_SCOPE_SINGLE, PERCEPTHOR_AUTH_SCOPE_MANAGEMENT

from .legacy import percepthor_encode_optional
from .routes import AUTH_ROUTE_DELETE
from .routes import auth_route_create, auth_route_create_action, auth_route_create_role
from .routes import auth_route_create_service, auth_route_create_permissions

__all__ = [
	"percepthor_auth_route", "percepthor_group_authenticate", "percepthor_group_configure",
	"percepthor_group_root_set", "percepthor_group_create", "percepthor_subgroup_create",
	"percepthor_endpoint_authenticate", "percepthor_endpoint_settings_check",
	"percepthor_route", "percepthor_group_route", "PercepthorGroup"
]

TEXT_ENCODING = "utf-8"

def percepthor_auth_route (
	action: str | None = None, role: str | None = None, service: bool = False,
	management: int | None = None, single: int | None = None
) -> int:
	"""Creates the AuthRoute that libauth uses to authenticate an endpoint.

	The first one of single, management, service, role and action that is given is used.

	Args:
		action: The action of the role of the token, or the action of a permissions route.
		role: The role that the token needs.
		service: True to only accept the token of a service.
		management: A PERMISSIONS_TYPE_* value for a management permissions route.
		single: A PERMISSIONS_TYPE_* value for a single permissions route.

	Returns:
		The AuthRoute, a route that only needs a token when nothing is given.
	"""
	auth_route = None

	encoded_action = percepthor_encode_optional (action)

	if (single is not None):
		auth_route = auth_route_create_permissions (PERCEPTHOR_AUTH_SCOPE_SINGLE, single, encoded_action)

	elif (management is not None):
		auth_route = auth_route_create_permissions (PERCEPTHOR_AUTH_SCOPE_MANAGEMENT, management, encoded_action)

	elif (service):
		auth_route = auth_route_create_service ()

	elif (role):
		auth_route = auth_route_create_role (encoded_action, role.encode (TEXT_ENCODING))

	elif (action):
		auth_route = auth_route_create_action (encoded_action)

	else:
		auth_route = auth_route_create ()

	return auth_route

def percepthor_group_authenticate (group: int) -> None:
	"""Authenticates the endpoints of a group with a token.

	An endpoint can set its own action, role, service or permissions.

	Args:
		group: The HttpGroup.
	"""
	http_group_set_auth (group, HTTP_ROUTE_AUTH_TYPE_CUSTOM)
	http_group_set_authentication_handler (group, percepthor_custom_authentication_handler)
	http_group_set_custom_data (group, auth_route_create (), AUTH_ROUTE_DELETE)

def percepthor_group_configure (
	group: int,
	cors: bool | None = None, etag: bool | None = None, compression: bool | None = None
) -> None:
	"""Sets the settings of a group that were given, its subgroups and endpoints inherit them.

	Args:
		group: The HttpGroup.
		cors: True to add the Access-Control-Allow-Origin of a whitelisted origin to every response.
		etag: True to answer the GET requests with 304 when their If-None-Match matches the body.
		compression: True to send the bodies with gzip when the request accepts it.
	"""
	if (cors is not None):
		http_group_set_cors (group, cors)

	if (etag is not None):
		http_group_set_etag (group, etag)

	if (compression is not None):
		http_group_set_compression (group, compression)

def percepthor_group_root_set (group: int, method: int | None, handler: Callable | None, **settings) -> None:
	"""Adds the endpoint of the group itself when there is a handler.

	Args:
		group: The HttpGroup.
		method: A REQUEST_METHOD_* value, or None.
		handler: The handler, or None.
		**settings: The settings of percepthor_route ().

	Raises:
		ValueError: If there is a method without a handler or a handler without a method.
	"""
	if ((method is None) != (handler is None)):
		raise ValueError ("The root of a group needs both its method and its handler")

	if (group and (handler is not None)):
		percepthor_group_route (group, method, handler, **settings)

def percepthor_group_create (
	http_cerver: int, prefix: str,
	method: int | None = None, handler: Callable | None = None,
	authenticated: bool = True, **settings
) -> int:
	"""Creates a top level group, like "api/tickets".

	Args:
		http_cerver: The HttpCerver.
		prefix: The prefix of the group.
		method: The method of the endpoint of the group itself, like GET /api/tickets.
		handler: The handler of the endpoint of the group itself.
		authenticated: True (the default) to authenticate its endpoints with a token.
		**settings: The settings of the endpoint of the group itself.

	Returns:
		The HttpGroup.

	Raises:
		ValueError: If cerver could not create the group.
	"""
	group = http_cerver_group_create (http_cerver, prefix.encode (TEXT_ENCODING))

	if (not group):
		raise ValueError (f"Failed to create the group {prefix}")

	if (authenticated):
		percepthor_group_authenticate (group)

	percepthor_group_root_set (group, method, handler, **settings)

	return group

def percepthor_subgroup_create (
	parent: int, prefix: str,
	method: int | None = None, handler: Callable | None = None, **settings
) -> int:
	"""Creates a group inside another one, it inherits its authentication.

	Args:
		parent: The parent HttpGroup.
		prefix: The prefix of the group, relative to its parent.
		method: The method of the endpoint of the group itself.
		handler: The handler of the endpoint of the group itself.
		**settings: The settings of the endpoint of the group itself.

	Returns:
		The HttpGroup.

	Raises:
		ValueError: If cerver could not create the group.
	"""
	group = http_group_create (parent, prefix.encode (TEXT_ENCODING))

	if (not group):
		raise ValueError (f"Failed to create the group {prefix}")

	percepthor_group_root_set (group, method, handler, **settings)

	return group

def percepthor_endpoint_authenticate (
	endpoint: int,
	action: str | None = None, role: str | None = None, service: bool = False,
	management: int | None = None, single: int | None = None,
	public: bool = False
) -> None:
	"""Sets the authentication of an endpoint.

	A public endpoint is not authenticated. A single endpoint authenticates itself with
	percepthor_single_authentication () from its handler.

	Args:
		endpoint: The HttpEndpoint.
		action: The action of the role of the token, or the action of a permissions route.
		role: The role that the token needs.
		service: True to only accept the token of a service.
		management: A PERMISSIONS_TYPE_* value for a management permissions route.
		single: A PERMISSIONS_TYPE_* value for a single permissions route.
		public: True for an endpoint that is not authenticated.
	"""
	if (public):
		http_endpoint_set_auth (endpoint, HTTP_ROUTE_AUTH_TYPE_NONE)

	elif (single is not None):
		http_endpoint_set_auth (endpoint, HTTP_ROUTE_AUTH_TYPE_NONE)
		http_endpoint_set_custom_data (
			endpoint, percepthor_auth_route (action = action, single = single), AUTH_ROUTE_DELETE
		)

	else:
		http_endpoint_set_auth (endpoint, HTTP_ROUTE_AUTH_TYPE_CUSTOM)
		http_endpoint_set_authentication_handler (endpoint, percepthor_custom_authentication_handler)
		http_endpoint_set_custom_data (
			endpoint,
			percepthor_auth_route (action, role, service, management),
			AUTH_ROUTE_DELETE
		)

def percepthor_endpoint_settings_check (settings: dict) -> None:
	"""Checks the settings of an endpoint, its auth is the one that percepthor sets.

	Args:
		settings: The settings of http_endpoint_configure ().

	Raises:
		ValueError: If the settings have an auth, it would replace the one of percepthor.
	"""
	if ("auth" in settings):
		raise ValueError ("The auth of a percepthor endpoint is set by its action, role, service, management, single or public")

def percepthor_route (
	group: int, method: int, path: str, handler: Callable,
	action: str | None = None, role: str | None = None, service: bool = False,
	management: int | None = None, single: int | None = None,
	public: bool = False, **settings
) -> int | None:
	"""Adds an endpoint to a group with its own authentication.

	Args:
		group: The HttpGroup.
		method: A REQUEST_METHOD_* value.
		path: The path relative to the group, with ":name" params.
		handler: A Python function (http_receive, request) or an HttpHandler.
		action: The action of the role of the token, or the action of a permissions route.
		role: The role that the token needs.
		service: True to only accept the token of a service.
		management: A PERMISSIONS_TYPE_* value for a management permissions route.
		single: A PERMISSIONS_TYPE_* value for a single permissions route.
		public: True for an endpoint that is not authenticated.
		**settings: The other settings of http_endpoint_configure () (modifier, max_body_size,
			cors, etag, compression, before, after).

	Returns:
		The HttpEndpoint, None on error (the cerver will not start).

	Raises:
		ValueError: If the settings have an auth.
	"""
	percepthor_endpoint_settings_check (settings)

	endpoint = http_group_route_add (
		group, method, path.encode (TEXT_ENCODING), http_handler (handler)
	)

	if (endpoint):
		percepthor_endpoint_authenticate (
			endpoint, action, role, service, management, single, public
		)

		http_endpoint_configure (endpoint, **settings)

	return endpoint

def percepthor_group_route (
	group: int, method: int, handler: Callable,
	action: str | None = None, role: str | None = None, service: bool = False,
	management: int | None = None, single: int | None = None,
	public: bool = False, **settings
) -> int | None:
	"""Adds the endpoint of a method in the path of the group itself, like GET /api/tickets.

	Args:
		group: The HttpGroup.
		method: A REQUEST_METHOD_* value.
		handler: A Python function (http_receive, request) or an HttpHandler.
		action: The action of the role of the token, or the action of a permissions route.
		role: The role that the token needs.
		service: True to only accept the token of a service.
		management: A PERMISSIONS_TYPE_* value for a management permissions route.
		single: A PERMISSIONS_TYPE_* value for a single permissions route.
		public: True for an endpoint that is not authenticated.
		**settings: The other settings of http_endpoint_configure ().

	Returns:
		The HttpEndpoint, None on error (the cerver will not start).

	Raises:
		ValueError: If the settings have an auth.
	"""
	percepthor_endpoint_settings_check (settings)

	endpoint = http_group_root_add (group, method, http_handler (handler))

	if (endpoint):
		percepthor_endpoint_authenticate (
			endpoint, action, role, service, management, single, public
		)

		http_endpoint_configure (endpoint, **settings)

	return endpoint

class PercepthorGroup (HttpGroup):
	"""A group of authenticated routes with decorators.

	Example:
		api = PercepthorGroup.create (http_cerver, "api/tickets")

		@api.post ("/:id/close", action="tickets.close")
		def ticket_close (http_receive, request):
			...

	The handlers keep their signature (http_receive, request), and the decorators take the
	settings of percepthor_route ().
	"""

	@classmethod
	def create (
		cls, http_cerver: int, prefix: str,
		method: int | None = None, handler: Callable | None = None,
		authenticated: bool = True, **settings
	) -> "PercepthorGroup":
		"""Creates a top level group, see percepthor_group_create ().

		Returns:
			The PercepthorGroup.
		"""
		return cls (percepthor_group_create (
			http_cerver, prefix, method, handler, authenticated, **settings
		))

	def subgroup (
		self, prefix: str,
		method: int | None = None, handler: Callable | None = None, **settings
	) -> "PercepthorGroup":
		"""Creates a group inside this one, see percepthor_subgroup_create ().

		Returns:
			The PercepthorGroup.
		"""
		return PercepthorGroup (percepthor_subgroup_create (
			self.group, prefix, method, handler, **settings
		))

	def add (self, method: int, path: str, handler: Callable, **settings) -> int | None:
		"""Adds an endpoint to the group, see percepthor_route ().

		Returns:
			The HttpEndpoint, None on error.
		"""
		return percepthor_route (self.group, method, path, handler, **settings)

	def root (self, method: int, handler: Callable, **settings) -> int | None:
		"""Adds the endpoint of the group itself, see percepthor_group_route ().

		Returns:
			The HttpEndpoint, None on error.
		"""
		return percepthor_group_route (self.group, method, handler, **settings)

	def configure (
		self, cors: bool | None = None, etag: bool | None = None, compression: bool | None = None
	) -> "PercepthorGroup":
		"""Sets the settings that the endpoints of the group inherit, see percepthor_group_configure ().

		Returns:
			The group itself.
		"""
		percepthor_group_configure (self.group, cors, etag, compression)
		return self
