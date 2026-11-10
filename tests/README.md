# pypercepthor tests

The suite of the package, in the variant of a Python package of
`percepthor-backend/docs/conventions/testing.md` §13. It runs only inside its image: cerver and libauth are
compiled there from their local sources, and the working trees of pypercepthor, pycerver and auth-service are
mounted and go first in `PYTHONPATH`, so the suite never tests an installed copy.

| Tier | What | Needs |
|---|---|---|
| `unit/` | The validators and the body reader, every binding against the prototypes of the headers of libauth (`test_bindings.py`), its enums against the probe of the image (`probe/probe.c`, `test_constants.py`), the `__all__` of every module (`test_exports.py`), the auth values of the routes, the version, the symbols the backend imports, hypothesis | the image |
| `integration/` | A real web cerver created and compiled, never started: groups, subgroups, the auth of every endpoint, the legacy routes with plain Python handlers, the admin routes, a real request without body | the image |
| `e2e/` | A started cerver whose routes authenticate with libauth against the working tree of auth-service, with JWT RS256 minted by the test and the keys of Redis that the other services write | `packages-test-mongo` (:27022) and `packages-test-redis` (:6396) |

## Running

```bash
./build.sh                          # itpercepthor/pypercepthor:tests (cerver, libauth, auth-service requirements)
./run.sh                            # unit + integration
./run.sh mongo && ./run.sh redis    # the packages-tests compose, shared with the suite of py-cerver
./run.sh e2e                        # auth-service as a subprocess, one cerver in a thread
./run.sh unit -k body               # a tier forwards what follows it to pytest

SANITIZER=address,undefined ./build.sh
./run.sh asan                       # unit + integration with libcerver and libauth instrumented
./run.sh asan e2e/                  # the e2e too, auth-service inherits the preload
./run.sh fuzz                       # hypothesis with the nightly profile (5000 examples)
./run.sh repeat e2e/ 20             # stops at the first failure
./run.sh coverage                   # tests/htmlcov
```

`TESTS_IMAGE=<tag>` builds and runs another tag, and `AUTH_DIR`, `CERVER_DIR`, `PYCERVER_DIR` and
`AUTH_SERVICE_DIR` point to other trees: that is how a test is seen failing against the code before its fix.

## Rules

- Nothing of cerver, libauth or the package is stubbed; a getter of cerver is patched only to a real
  `String` or to a real NULL `StringPointer`, which is what libcerver returns.
- The RSA keys of the e2e are generated in a temporary directory on every run: nothing generated is committed.
- The e2e runs auth-service as another process, like in production, and its own cerver in a thread of pytest
  (before cerver 2.0b-60 a process could run only one HTTP cerver, `docs/backlog/cerver-findings.md` §14).
- The legacy routes release their AuthRoute with the C address of `auth_route_delete ()`
  (`AUTH_ROUTE_DELETE_ROUTE`), never with a python callback; the admin routes share one AuthRoute that cerver
  releases once, so they do not get one.
- A new symbol that the backend imports from `percepthor` goes in `unit/test_backend_exports.py`.
