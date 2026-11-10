# Create PyPercepthor Release

0. Update the version in `percepthor/version.py` (with its date and time, and the versions of libauth and pycerver
that it binds) and in `version.txt`, the changes of the release in `CHANGELOG.md`, and its breaking changes in
`incompatibilities.md`

1. Run every tier against the cerver and the libauth of the release, normal and with the sanitizers

```
bash tests/build.sh
SANITIZER=address,undefined bash tests/build.sh
bash tests/run.sh
bash tests/run.sh asan
bash tests/run.sh e2e
```

2. Build, from a clean tree

```
rm -rf build dist
python3 -m build
```

3. Upload

```
python3 -m twine upload dist/*
```
