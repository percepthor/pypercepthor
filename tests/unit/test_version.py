"""Unit tests for version.py - the version prints of pypercepthor and libauth.

Bugs these tests fixed:
- pypercepthor_version_print_version_id () and _name () read version.id and version.name
  of a dict, so they raised AttributeError
"""

import pytest

from percepthor import PERCEPTHOR_VERSION
from percepthor import PERCEPTHOR_VERSION_NAME
from percepthor import percepthor_libauth_version_print_full
from percepthor import percepthor_libauth_version_print_version_id
from percepthor import percepthor_libauth_version_print_version_name
from percepthor import pypercepthor_version_print_full
from percepthor import pypercepthor_version_print_version_id
from percepthor import pypercepthor_version_print_version_name
from percepthor import version

pytestmark = [pytest.mark.unit]

class TestVersion:

	def test_version_values (self):
		assert version["id"] == PERCEPTHOR_VERSION
		assert version["name"] == PERCEPTHOR_VERSION_NAME

	@pytest.mark.parametrize ("version_print", [
		pypercepthor_version_print_full,
		pypercepthor_version_print_version_id,
		pypercepthor_version_print_version_name,
		percepthor_libauth_version_print_full,
		percepthor_libauth_version_print_version_id,
		percepthor_libauth_version_print_version_name
	])
	def test_print (self, version_print):
		version_print ()
