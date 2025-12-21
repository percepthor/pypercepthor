"""The AuthService of a cerver: the id and the name of the service and the address of the
auth service. It is the custom data of the HTTP cerver of the service.
"""

from ctypes import c_void_p, c_char_p

from ..lib import auth_function

__all__ = [
	"auth_service_new", "auth_service_delete", "auth_service_create", "auth_service_print"
]

auth_service_new = auth_function (
	"auth_service_new", [], c_void_p,
	"""Allocates an empty AuthService.

	Returns:
		The AuthService, released with auth_service_delete (), None on error.
	"""
)

auth_service_delete = auth_function (
	"auth_service_delete", [c_void_p], None,
	"""Releases an AuthService.

	Args:
		auth_service: The AuthService, None does nothing.
	"""
)

auth_service_create = auth_function (
	"auth_service_create", [c_char_p, c_char_p, c_char_p], c_void_p,
	"""Creates the AuthService of a service, a value longer than its buffer is truncated.

	Args:
		service_id: The id of the service as bytes, None for a service without service routes.
		service_name: The name of the service as bytes, the source of its requests.
		auth_service_address: The url of the auth service as bytes.

	Returns:
		The AuthService, released with auth_service_delete (), None on error.
	"""
)

auth_service_print = auth_function (
	"auth_service_print", [c_void_p], None,
	"""Prints the values of an AuthService.

	Args:
		auth_service: The AuthService, None does nothing.
	"""
)
