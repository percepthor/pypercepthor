"""Builders shared by the tiers of the suite."""

from ctypes import pointer

from cerver.types import String
from cerver.types import StringPointer

ID_ORGANIZATION = "507f1f77bcf86cd799439011"
ID_ROLE = "507f1f77bcf86cd799439012"
ID_USER = "507f1f77bcf86cd799439013"
ID_TOKEN = "507f1f77bcf86cd799439014"
ID_RESOURCE = "507f1f77bcf86cd799439015"
ID_SERVICE = "507f1f77bcf86cd799439016"

def build_string (content: bytes):
	"""A real cerver String with the content, as the getters of cerver return it."""
	return pointer (String (len (content), len (content), content))

def build_null_string ():
	"""The NULL String pointer that a getter of cerver returns for a missing value."""
	return StringPointer ()
