# Routes

`from percepthor import ...` (the names of `percepthor.routes`)

## Groups and endpoints

``` python
tickets = PercepthorGroup.create (http_cerver, "api/tickets", REQUEST_METHOD_GET, tickets_list)

@tickets.post ("/", action="tickets.create")
def ticket_create (http_receive, request):
	...

reports = tickets.subgroup ("reports", role="manager")
```

A `PercepthorGroup` is an `HttpGroup` of pycerver whose endpoints are authenticated with a token by default
(`authenticated=False` creates one without it). Its decorators (`get`, `post`, `put`, `patch`, `delete`, `head`,
`options`), `add ()` and `root ()` take the authentication of the endpoint:

| Setting | The endpoint needs |
|---|---|
| (none) | A valid token |
| `action="..."` | An action of the role of the token |
| `role="..."` | A role, and the `action` too when it is given |
| `service=True` | The token of a service |
| `management=PERMISSIONS_TYPE_*` | The permissions over every resource of the type, with the `action` |
| `single=PERMISSIONS_TYPE_*` | The permissions over a single resource, checked by its handler (see [auth.md](auth.md)) |
| `public=True` | Nothing |

When several of them are given, the first one of `single`, `management`, `service`, `role` and `action` is used. The
other settings are the ones of pycerver (`modifier`, `max_body_size`, `cors`, `etag`, `compression`, `before`,
`after`); an `auth` setting raises `ValueError`, the auth of an endpoint is the one percepthor sets.

The functions behind them are `percepthor_group_create`, `percepthor_subgroup_create`, `percepthor_route`,
`percepthor_group_route`, `percepthor_endpoint_authenticate`, `percepthor_group_configure` and `percepthor_auth_route`
(`percepthor.routes.groups`).

## The routes of the first API

``` python
route = percepthor_action_route_create (REQUEST_METHOD_POST, "api/tickets", ticket_create, "tickets.create")
http_cerver_route_register (http_cerver, route)
```

`percepthor_route_create`, `percepthor_action_route_create`, `percepthor_role_route_create`,
`percepthor_service_route_create`, `percepthor_management_route_create` and `percepthor_single_route_create`
(`percepthor.routes.legacy`) create a route with its `AuthRoute`, which cerver releases with the route. The handler is
a plain Python function or an `HttpHandler`, kept for as long as the process lives.

## AuthRoute

`auth_route_create`, `auth_route_create_action`, `auth_route_create_role`, `auth_route_create_service`,
`auth_route_create_permissions` and `auth_route_delete` (`percepthor.routes.routes`) are the functions of libauth.
`AUTH_ROUTE_DELETE` is the C address of `auth_route_delete` for the setters of a group or an endpoint, and
`AUTH_ROUTE_DELETE_ROUTE` the same for a route of the first API.

## Admin routes

`percepthor_admin_routes_configuration (http_cerver)` enables the admin routes of cerver (`/cerver/...`),
authenticated with a token.
