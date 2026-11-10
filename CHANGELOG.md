## General
- Released pypercepthor 0.7, for libauth 0.5 & pycerver 1.0: the breaking changes from 0.6.2 are in incompatibilities.md
- Split the package in the auth, routes & validations subpackages, each module with an explicit __all__
- Loading libauth from AUTH_LIBRARY, /usr/local/lib or the system linker, with an AuthLibraryError when it is missing
- Declaring every binding with its argtypes, restype & docstring in a registry (auth_functions)
- Added the docstrings of every public function in Google style
- Replaced setup.py & setup.cfg with a PEP 621 pyproject.toml, with py.typed & the LICENSE

## Bindings
- Fixed the void functions without restype None & the functions without arguments without argtypes
- Fixed the libauth version functions, that had neither argtypes nor restype
- Added the token types & percepthor_token_type_to_string ()

## Routes
- Added the groups & endpoints of the routes tree: PercepthorGroup, percepthor_route () & percepthor_group_* ()
- The routes of the first API keep their handler, so they take a plain Python function
- Releasing the AuthRoute of the admin routes

## Validations
- Reading the query values & the body with their length, a NUL byte no longer cuts them
- Any error of a cast of a query value makes it invalid, without catching KeyboardInterrupt & SystemExit
- percepthor_query_optional_value_from_params () takes the errors of the request

## Tests
- Added the unit, integration & e2e tiers, the bindings checked against the headers of libauth & its enums against a probe
- Running every tier with Python 3.14, gcc 16.2 & the address & undefined sanitizers
