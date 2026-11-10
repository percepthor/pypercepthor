"""The authentication handlers of libauth.

``percepthor_custom_authentication_handler`` is a C function with the signature of an
HttpAuthenticationHandler of cerver, so it is given directly to the setters of cerver
(it is not a Python callback, there is nothing to keep).
"""

from ctypes import c_void_p, c_char_p, c_uint

from ..lib import auth_function

__all__ = [
	"percepthor_single_authentication", "percepthor_custom_authentication_handler"
]

percepthor_single_authentication = auth_function (
	"percepthor_single_authentication", [c_void_p, c_void_p, c_char_p], c_uint,
	"""Authenticates a request with the permissions of a single resource.

	It is called by the handler of a single permissions route, with the resource of the
	request (like a param of its path). When the auth service accepts it, the
	PercepthorAuth is the custom data of the request.

	Args:
		http_receive: The HttpReceive of the request.
		request: The request.
		resource: The resource, as bytes.

	Returns:
		0 when the request was authenticated, 1 otherwise.
	"""
)

percepthor_custom_authentication_handler = auth_function (
	"percepthor_custom_authentication_handler", [c_void_p, c_void_p], c_uint,
	"""The authentication handler of the routes of a cerver.

	It authenticates the request with the AuthRoute of the route (its custom data) and the
	AuthService of the cerver (the custom data of the HTTP cerver).

	Args:
		http_receive: The HttpReceive of the request.
		request: The request.

	Returns:
		0 when the request was authenticated, 1 otherwise.
	"""
)
