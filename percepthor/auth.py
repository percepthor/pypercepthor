from .lib import lib

from ctypes import c_void_p, c_char_p, c_int, c_uint, c_bool

# auth
PERCEPTHOR_AUTH_TYPE_NONE = 0
PERCEPTHOR_AUTH_TYPE_SINGLE = 1
PERCEPTHOR_AUTH_TYPE_MANAGEMENT = 2
PERCEPTHOR_AUTH_TYPE_TOKEN = 3

percepthor_auth_type_to_string = lib.percepthor_auth_type_to_string
percepthor_auth_type_to_string.argtypes = [c_int]
percepthor_auth_type_to_string.restype = c_char_p

percepthor_auth_delete = lib.percepthor_auth_delete
percepthor_auth_delete.argtypes = [c_void_p]

percepthor_auth_get_type = lib.percepthor_auth_get_type
percepthor_auth_get_type.argtypes = [c_void_p]
percepthor_auth_get_type.restype = c_int

percepthor_auth_get_organization = lib.percepthor_auth_get_organization
percepthor_auth_get_organization.argtypes = [c_void_p]
percepthor_auth_get_organization.restype = c_char_p

percepthor_auth_get_action = lib.percepthor_auth_get_action
percepthor_auth_get_action.argtypes = [c_void_p]
percepthor_auth_get_action.restype = c_char_p

percepthor_auth_get_admin = lib.percepthor_auth_get_admin
percepthor_auth_get_admin.argtypes = [c_void_p]
percepthor_auth_get_admin.restype = c_bool

percepthor_auth_get_permissions = lib.percepthor_auth_get_permissions
percepthor_auth_get_permissions.argtypes = [c_void_p]
percepthor_auth_get_permissions.restype = c_void_p

percepthor_auth_permissions_iter_start = lib.percepthor_auth_permissions_iter_start
percepthor_auth_permissions_iter_start.argtypes = [c_void_p]
percepthor_auth_permissions_iter_start.restype = c_bool

percepthor_auth_permissions_iter_get_next = lib.percepthor_auth_permissions_iter_get_next
percepthor_auth_permissions_iter_get_next.argtypes = [c_void_p]
percepthor_auth_permissions_iter_get_next.restype = c_void_p

percepthor_auth_create = lib.percepthor_auth_create
percepthor_auth_create.argtypes = [c_int]
percepthor_auth_create.restype = c_void_p

percepthor_single_authentication = lib.percepthor_single_authentication
percepthor_single_authentication.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p]
percepthor_single_authentication.restype = c_uint

percepthor_management_authentication = lib.percepthor_management_authentication
percepthor_management_authentication.argtypes = [c_void_p, c_void_p]
percepthor_management_authentication.restype = c_uint

# permissions
permissions_get_organization = lib.permissions_get_organization
permissions_get_organization.argtypes = [c_void_p]
permissions_get_organization.restype = c_char_p

permissions_print = lib.permissions_print
permissions_print.argtypes = [c_void_p]

permissions_has_action = lib.permissions_has_action
permissions_has_action.argtypes = [c_void_p, c_char_p]
permissions_has_action.restype = c_bool

# service
auth_service_new = lib.auth_service_new
auth_service_new.restype = c_void_p

auth_service_delete = lib.auth_service_delete
auth_service_delete.argtypes = [c_void_p]

auth_service_create = lib.auth_service_create
auth_service_create.argtypes = [c_char_p, c_char_p, c_char_p]
auth_service_create.restype = c_void_p

auth_service_print = lib.auth_service_print
auth_service_print.argtypes = [c_void_p]

# version
percepthor_libauth_version_print_full = lib.percepthor_libauth_version_print_full
percepthor_libauth_version_print_version_id = lib.percepthor_libauth_version_print_version_id
percepthor_libauth_version_print_version_name = lib.percepthor_libauth_version_print_version_name
