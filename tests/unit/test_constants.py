"""Every constant of the enums of libauth against its value in the headers.

The probe of the image (tests/probe/probe.c) prints each value of the maps of the headers,
compiled from the same sources as libauth.so.
"""

import subprocess

import pytest

import percepthor

pytestmark = [pytest.mark.unit]

PROBE = "/opt/percepthor/probe"

def probe_values () -> dict:
	"""Returns every value that the probe prints, by its name."""
	output = subprocess.run ([PROBE], capture_output=True, text=True, check=True).stdout

	values = dict ()
	for line in output.splitlines ():
		name, value = line.split ()
		values[name] = int (value)

	return values

PROBE_VALUES = probe_values ()

class TestConstants:

	def test_the_probe_printed_every_enum (self):
		prefixes = ("PERCEPTHOR_AUTH_TYPE_", "PERCEPTHOR_AUTH_SCOPE_", "PERMISSIONS_TYPE_", "PERCEPTHOR_TOKEN_TYPE_")

		assert all (any (name.startswith (prefix) for name in PROBE_VALUES) for prefix in prefixes)

	@pytest.mark.parametrize ("name", sorted (PROBE_VALUES))
	def test_constant (self, name):
		assert getattr (percepthor, name) == PROBE_VALUES[name]

	def test_every_constant_of_the_package_is_in_the_headers (self):
		prefixes = ("PERCEPTHOR_AUTH_TYPE_", "PERCEPTHOR_AUTH_SCOPE_", "PERMISSIONS_TYPE_", "PERCEPTHOR_TOKEN_TYPE_")
		constants = {name for name in percepthor.__all__ if (name.startswith (prefixes))}

		assert constants == set (PROBE_VALUES)
