# Auth

`from percepthor import ...` (the names of `percepthor.auth`)

## The AuthService of a service

``` python
auth_service = auth_service_create (b"507f1f77bcf86cd799439010", b"tickets", b"http://auth:5000/api/auth/check")

http_cerver_set_custom_data (http_cerver, auth_service)
```

The id of the service is only needed by its service routes, the name is the source of every request to the auth
service. `auth_service_delete ()` releases it after the cerver stopped.

## The values of an authenticated request

When libauth authenticates a request, its `PercepthorAuth` is the custom data of the request:

``` python
auth = http_request_get_custom_data (request)

user = percepthor_auth_get_token_user (auth)                 # bytes, None for NULL
organization = percepthor_auth_get_token_organization (auth)
admin = percepthor_auth_get_admin (auth)                     # bool
mask = percepthor_auth_get_mask (auth)                       # the actions mask of a service route
```

| Module | What it has |
|---|---|
| `percepthor.auth.values` | `PERCEPTHOR_AUTH_TYPE_*`, `PERCEPTHOR_AUTH_SCOPE_*`, `percepthor_auth_get_*`, `percepthor_auth_permissions_iter_*`, `percepthor_auth_create` / `_delete` and `percepthor_auth_print_token` |
| `percepthor.auth.handlers` | `percepthor_custom_authentication_handler` and `percepthor_single_authentication` |
| `percepthor.auth.permissions` | `PERMISSIONS_TYPE_*`, `permissions_get_resource`, `permissions_has_action` and `permissions_print` |
| `percepthor.auth.tokens` | `PERCEPTHOR_TOKEN_TYPE_*` and `percepthor_token_type_to_string` |
| `percepthor.auth.services` | `auth_service_create`, `auth_service_new`, `auth_service_delete` and `auth_service_print` |

Every getter accepts `None`, the custom data of a request that libauth did not authenticate, and the strings are
`bytes`.

## Permissions

A management route gets the resources over which the user has its action:

``` python
resources = []

if (percepthor_auth_permissions_iter_start (auth)):
	permissions = percepthor_auth_permissions_iter_get_next (auth)
	while (permissions):
		if (permissions_has_action (permissions, b"tickets.update")):
			resources.append (permissions_get_resource (permissions).decode ("utf-8"))

		permissions = percepthor_auth_permissions_iter_get_next (auth)
```

The state of the iteration lives in the `PercepthorAuth`, so two threads can not iterate the same one at the same time.
`percepthor_auth_get_admin (auth)` is `True` for a super admin, who has every resource.

## Single permissions

A single endpoint (`single=PERMISSIONS_TYPE_*`) is not authenticated before its handler: the handler authenticates
the request with the resource of its path.

``` python
@tickets.get ("/:id", single=PERMISSIONS_TYPE_ORGANIZATION, action="tickets.read")
def ticket_get (http_receive, request):
	ticket_id = http_request_get_param_string (request, 0)

	if (not percepthor_single_authentication (http_receive, request, ticket_id.encode ("utf-8"))):
		...
```
