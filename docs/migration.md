# Migration

The breaking changes are in [incompatibilities.md](../incompatibilities.md). The steps to move a service from 0.6.2
to 0.7:

1. Install libauth 0.5, pycerver 1.0 and cerver 2.0b-64 or newer in the image of the service, and pypercepthor 0.7.
2. Keep importing every name from the package itself (`from percepthor import ...`); an import of an old module
   (`percepthor.validation`, `percepthor.service`, `percepthor.permissions`) moves to its new one.
3. Point the patches of the tests to the modules that use the names now:
   - `percepthor.routes.<name>` of the groups to `percepthor.routes.groups.<name>`;
   - `percepthor.validation.http_request_get_body` to `percepthor.validations.bodies.http_request_get_body`;
   - `percepthor.validation.http_query_pairs_get_value` to `percepthor.validations.queries.http_query_pairs_get_value`.
4. A fake body or query value of a test has to be a real `String` of cerver:

``` python
from ctypes import pointer
from cerver.types import String

def build_string (content: bytes):
	return pointer (String (len (content), len (content), content))
```

5. Import from their own packages what the old modules leaked (`json`, `ctypes`, the names of `cerver.http`).
