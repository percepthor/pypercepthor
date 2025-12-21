"""The permissions of a user over the resources of a type, as the auth service answers them
to a management permissions route.
"""

from ctypes import c_void_p, c_char_p, c_int, c_bool
from typing import TypeAlias

from ..lib import auth_function

__all__ = [
	"PermissionsType",
	"PERMISSIONS_TYPE_NONE", "PERMISSIONS_TYPE_SERVICE",
	"PERMISSIONS_TYPE_ORGANIZATION", "PERMISSIONS_TYPE_PROJECT",
	"permissions_type_to_string", "permissions_get_resource",
	"permissions_print", "permissions_has_action"
]

PermissionsType: TypeAlias = c_int # type: ignore

PERMISSIONS_TYPE_NONE = 0
PERMISSIONS_TYPE_SERVICE = 1
PERMISSIONS_TYPE_ORGANIZATION = 2
PERMISSIONS_TYPE_PROJECT = 3

permissions_type_to_string = auth_function (
	"permissions_type_to_string", [PermissionsType], c_char_p,
	"""Returns the name of a permissions type.

	Args:
		type: A PERMISSIONS_TYPE_* value.

	Returns:
		The name as bytes, b"None" for an unknown type.
	"""
)

permissions_get_resource = auth_function (
	"permissions_get_resource", [c_void_p], c_char_p,
	"""Returns the resource of the permissions.

	Args:
		permissions: The Permissions, like one of percepthor_auth_permissions_iter_get_next ().

	Returns:
		The resource as bytes, None for NULL.
	"""
)

permissions_print = auth_function (
	"permissions_print", [c_void_p], None,
	"""Prints the resource and the actions of the permissions.

	Args:
		permissions: The Permissions, None does nothing.
	"""
)

permissions_has_action = auth_function (
	"permissions_has_action", [c_void_p, c_char_p], c_bool,
	"""Checks if the permissions allow an action.

	Args:
		permissions: The Permissions.
		action: The action, as bytes.

	Returns:
		True when the action is one of the actions of the resource.
	"""
)
