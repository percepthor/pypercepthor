# Incompatibilities

The changes of each version that can break code built with the version before it, the newest first.
Unlike `CHANGELOG.md`, which only has the current version, every entry stays here.

## 0.7 (from 0.6.2)

0.7 needs libauth 0.5 and pycerver 1.0 (cerver 2.0b-64 or newer).

### Modules

The package is split in subpackages. Every public name is still importable from the package itself
(`from percepthor import ...`), so only the imports and the patches of the old modules break:

| 0.6.2 | 0.7 |
|---|---|
| `percepthor.auth` (a module) | `percepthor.auth.values` (the PercepthorAuth) and `percepthor.auth.handlers` (the authentication handlers); `percepthor.auth` is a subpackage |
| `percepthor.permissions` | `percepthor.auth.permissions` |
| `percepthor.service` | `percepthor.auth.services` |
| `percepthor.routes` (a module) | `percepthor.routes.routes` (the AuthRoute), `.legacy` (`percepthor_*_route_create`), `.groups` (`PercepthorGroup`, `percepthor_route`, `percepthor_group_*`, `percepthor_endpoint_*`) and `.admin`; `percepthor.routes` is a subpackage |
| `percepthor.validation` | `percepthor.validations.queries` (`percepthor_query_*`) and `percepthor.validations.bodies` (`percepthor_body_json_load`, `percepthor_handle_body_input`) |
| `percepthor.lib.lib` | the same, plus `auth_function ()` and `auth_functions`; `lib` is no longer exported by the package |

A `patch ()` of a test must target the module that uses the name now:

| 0.6.2 | 0.7 |
|---|---|
| `percepthor.validation.http_request_get_body` | `percepthor.validations.bodies.http_request_get_body` |
| `percepthor.validation.http_query_pairs_get_value` | `percepthor.validations.queries.http_query_pairs_get_value` |
| `percepthor.routes.http_group_route_add`, `.http_group_root_add`, `.percepthor_endpoint_authenticate`, `.http_endpoint_configure` | `percepthor.routes.groups.<name>` |
| `percepthor.routes.http_route_set_delete_custom_data` (and the other setters of the first API) | `percepthor.routes.legacy.<name>` |

The modules no longer leak what they import: `lib`, `json`, `ctypes` and the names of `cerver.http`, `cerver.types` and
`cerver.utils` have to be imported from their own packages.

### Behavior

- The library is loaded from `AUTH_LIBRARY`, then from `/usr/local/lib/libauth.so` and then with
  `ctypes.util.find_library`; when none loads, the import raises `AuthLibraryError` instead of an `OSError`
- The body and the values of the query are read with their length (`cerver.types.string_bytes ()`): a body with a NUL
  byte is not valid JSON anymore (0.6.2 read it up to the NUL), and a value with a NUL byte is read whole. The
  `http_request_get_body` and `http_query_pairs_get_value` of a test must return a real `String` of cerver
  (`pointer (String (len, len, content))`), an object that only has `.contents.str` is no longer read
- A cast of `percepthor_query_*_with_cast ()` that fails with any `Exception` makes the value invalid; 0.6.2 caught
  everything with a bare `except` (also `KeyboardInterrupt` and `SystemExit`)
- `percepthor_query_optional_value_from_params ()` takes the `errors` of the request as an optional argument: with
  them, a value that is not utf-8 is invalid; without them it is left out, as before
- An integer or a number with a default that is not utf-8 gets its default, 0.6.2 raised `UnicodeDecodeError`
- `percepthor_handle_body_input ()` is annotated as returning what the validator returns, `None` on error
- The routes of the first API (`percepthor_*_route_create ()`) keep their handler with `http_handler ()`: they take a
  plain Python function too
- `percepthor_admin_routes_configuration ()` registers `auth_route_delete` for the AuthRoute of the admin routes,
  which cerver releases at its teardown
- `auth_service_new ()` and `auth_service_delete ()` bind the functions that libauth 0.5 exports
- The void functions return `None` (they returned a meaningless integer), and the functions without arguments reject
  any argument
- `pypercepthor_version_print_*` print the versions of libauth and of pycerver too; `version` has their keys

### Packaging

- `setup.py` and `setup.cfg` were replaced by a PEP 621 `pyproject.toml`, with its dependency on `pycerver>=1.0`;
  Python 3.10 or newer
- The package has a `py.typed` and a `LICENSE`

### Services

The services that are migrated to 0.7 have to change (swept on 2026-11-09, every `from percepthor import X` of the
services still resolves):
- `tests/unit/test_api_routes.py` of gepp, balance, payloads and tickets: `ROUTES_PERCEPTHOR_MODULE` is
  `"percepthor.routes.groups"`
- `tests/e2e/client.py` of gepp, fifco, aviles, ccu and eltec: `import percepthor.validations.bodies`, its patch of
  `http_request_get_body`, and a fake body pointer that is a real `String`
- `tests/unit/test_lib_body_input.py` of payloads: the patch of `percepthor.validations.bodies.http_request_get_body`
