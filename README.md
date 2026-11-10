# PyPercepthor

pypercepthor (the `percepthor` package) is the Python wrapper of [libauth](https://github.com/percepthor/libauth), the
library with which the services of Percepthor authenticate their HTTP requests against the auth service, over
[pycerver](https://github.com/ermiry-com/py-cerver).

## Compatibility

| pypercepthor | libauth | pycerver | cerver | Python |
|---|---|---|---|---|
| 0.7 | 0.5 | 1.0 | 2.0b-64 or newer | 3.10 to 3.14 |

pypercepthor loads `libauth.so` at import time: from the path in the `AUTH_LIBRARY` environment variable, then from
`/usr/local/lib/libauth.so`, and then from the paths of the system linker. The breaking changes of each version are
in [incompatibilities.md](incompatibilities.md).

## Installation

1. Install cerver and libauth (`make install` of each one)
2. Install pycerver and pypercepthor

``` bash
pip install pycerver==1.0
pip install /path/to/pypercepthor
```

## Getting Started

The routes of a service are groups whose endpoints are authenticated by libauth:

``` python
from cerver.http import HTTP_STATUS_OK, http_cerver_get, http_cerver_set_custom_data
from cerver.http import http_request_get_custom_data, http_response_json_send

from percepthor import PercepthorGroup, auth_service_create, percepthor_auth_get_token_user

# the service, its name and the address of the auth service
auth_service = auth_service_create (b"507f1f77bcf86cd799439010", b"tickets", b"http://auth:5000/api/auth/check")
http_cerver_set_custom_data (http_cerver, auth_service)

# every endpoint of the group needs a token, and each one can require more
tickets = PercepthorGroup.create (http_cerver, "api/tickets")

@tickets.get ("/")
def tickets_list (http_receive, request):
	auth = http_request_get_custom_data (request)
	user = percepthor_auth_get_token_user (auth).decode ("utf-8")
	http_response_json_send (http_receive, HTTP_STATUS_OK, {"user": user})

@tickets.post ("/:id/close", action="tickets.close")
def ticket_close (http_receive, request):
	...
```

An endpoint can require an `action`, a `role`, the token of a `service`, the permissions over a `single` resource or
over every resource of a type (`management`), or be `public`. See [docs](docs/README.md).

## Packages

| Package | What it has |
|---|---|
| `percepthor.auth` | The values of an authenticated request (`percepthor_auth_get_*`), the authentication handlers, the permissions, the tokens and the `AuthService` |
| `percepthor.routes` | The `AuthRoute`, the groups and endpoints (`PercepthorGroup`, `percepthor_route`), the routes of the first API (`percepthor_*_route_create`) and the admin routes |
| `percepthor.validations` | The validators of the query (`percepthor_query_*`) and of the JSON body (`percepthor_handle_body_input`) |

Every name is importable from the package itself (`from percepthor import ...`), every module has an explicit
`__all__`, and every binding has its docstring.

## Tests

The tests run in Docker, against cerver and libauth compiled from their sources and the auth service for the e2e tier
(see [tests/README.md](tests/README.md)):

``` bash
bash tests/build.sh
bash tests/run.sh
bash tests/run.sh e2e
```
