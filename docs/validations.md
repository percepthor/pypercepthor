# Validations

`from percepthor import ...` (the names of `percepthor.validations`)

## The body

``` python
def ticket_create_input (body: dict, errors: dict) -> dict:
	return {"title": validate_body_string (body, "title", errors, max_len=128)}

errors = {}
values = percepthor_handle_body_input (request, ticket_create_input, errors)
```

`percepthor_handle_body_input ()` reads the body of the request with its length, loads it as JSON and calls the
validator of the route with the object and the errors. A missing body writes `errors["body"] = "Request body input is
required!"`, and a body that is not a JSON object `"Request body input is invalid."`; in both the validator is not
called and the result is `None`. `percepthor_body_json_load ()` does the loading of a body that was already read.

## The query

``` python
query = {}
errors = {}
params = http_request_get_query_params (request)

percepthor_query_value_from_params (query, params, "status", errors)
percepthor_query_int_value_from_params_with_default (query, params, "page", 1)
percepthor_query_value_from_params_with_cast (query, params, "user", ObjectId, errors)
```

The validators write the value in the dict of the query, by its name, or its error:

| Validator | Missing | Invalid |
|---|---|---|
| `percepthor_query_value_from_params`, `_int_`, `_float_`, `_bool_` | `Field <name> is required.` | `Field <name> is invalid.` |
| `percepthor_query_value_from_params_with_cast` | required | invalid when the cast raises any exception |
| `percepthor_query_optional_value_from_params` | left out | invalid with `errors`, left out without them |
| `percepthor_query_*_optional_value_from_params*` | left out | invalid |
| `percepthor_query_int_value_from_params_with_default`, `_float_` | the default | the default |

The typed validators of pycerver (`validate_query_*` and `validate_body_*` of `cerver.http`) return the values
instead of writing them, with their limits (lengths, ranges, choices, lists, dates).
