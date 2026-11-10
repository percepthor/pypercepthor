# Library

`percepthor.lib`

libauth is loaded when the package is imported, from:
1. the path in the `AUTH_LIBRARY` environment variable;
2. `/usr/local/lib/libauth.so`;
3. the paths of the system linker (`ctypes.util.find_library ("auth")`).

When none of them loads, the import raises `AuthLibraryError`. pycerver loads libcerver the same way
(`CERVER_LIBRARY`).

Every function of libauth is declared with `auth_function (name, argtypes, restype, doc)`, which registers it in
`auth_functions`. The suite checks each one against the prototype of its function in the installed headers of
libauth: the number and the ctypes of its arguments and of its result, that none is an `AUTH_PRIVATE` function, and
that every public function is bound or excluded with its reason.

| ctypes | C |
|---|---|
| `c_void_p` | A pointer to a struct of libauth or cerver; in Python an `int`, `None` for NULL |
| `c_char_p` | A `const char *`, `bytes` in Python |
| `c_int` | The enums (`PercepthorAuthType`, `PercepthorAuthScope`, `PermissionsType`, `PercepthorTokenType`) |
| `c_bool`, `c_uint`, `c_int64` | `bool`, `unsigned int`, `int64_t` |
