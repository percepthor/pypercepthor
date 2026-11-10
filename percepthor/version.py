"""The versions of pypercepthor and of the libauth that it wraps."""

from cerver.utils import LOG_TYPE_NONE, cerver_log_both

from .lib import auth_function

__all__ = [
	"PERCEPTHOR_VERSION", "PERCEPTHOR_VERSION_NAME", "PERCEPTHOR_VERSION_DATE",
	"PERCEPTHOR_VERSION_TIME", "PERCEPTHOR_VERSION_AUTHOR",
	"PERCEPTHOR_LIBAUTH_VERSION", "PERCEPTHOR_PYCERVER_VERSION",
	"version",
	"percepthor_libauth_version_print_full", "percepthor_libauth_version_print_version_id",
	"percepthor_libauth_version_print_version_name",
	"pypercepthor_version_print_full", "pypercepthor_version_print_version_id",
	"pypercepthor_version_print_version_name"
]

PERCEPTHOR_VERSION = "0.7"
PERCEPTHOR_VERSION_NAME = "Version 0.7"
PERCEPTHOR_VERSION_DATE = "26/12/2025"
PERCEPTHOR_VERSION_TIME = "17:27 CST"
PERCEPTHOR_VERSION_AUTHOR = "Erick Salas"

# the versions of libauth and of pycerver whose APIs this release binds
PERCEPTHOR_LIBAUTH_VERSION = "0.5"
PERCEPTHOR_PYCERVER_VERSION = "1.0"

version = {
	"id": PERCEPTHOR_VERSION,
	"name": PERCEPTHOR_VERSION_NAME,
	"date": PERCEPTHOR_VERSION_DATE,
	"time": PERCEPTHOR_VERSION_TIME,
	"author": PERCEPTHOR_VERSION_AUTHOR,
	"libauth": PERCEPTHOR_LIBAUTH_VERSION,
	"pycerver": PERCEPTHOR_PYCERVER_VERSION
}

percepthor_libauth_version_print_full = auth_function (
	"percepthor_libauth_version_print_full", [], None,
	"""Prints the version of libauth with its date and its author."""
)

percepthor_libauth_version_print_version_id = auth_function (
	"percepthor_libauth_version_print_version_id", [], None,
	"""Prints the version id of libauth."""
)

percepthor_libauth_version_print_version_name = auth_function (
	"percepthor_libauth_version_print_version_name", [], None,
	"""Prints the version name of libauth."""
)

def pypercepthor_version_print_full () -> None:
	"""Prints the version of pypercepthor with its date, its author and the versions it binds."""
	output = (
		"\nPyPercepthor Version: {name}\n"
		"Release Date: {date} - {time}\n"
		"Author: {author}\n"
		"libauth: {libauth} - pycerver: {pycerver}\n"
	).format (**version)

	cerver_log_both (LOG_TYPE_NONE, LOG_TYPE_NONE, output)

def pypercepthor_version_print_version_id () -> None:
	"""Prints the version id of pypercepthor."""
	cerver_log_both (LOG_TYPE_NONE, LOG_TYPE_NONE, f"\nPyPercepthor Version ID: {version['id']}\n")

def pypercepthor_version_print_version_name () -> None:
	"""Prints the version name of pypercepthor."""
	cerver_log_both (LOG_TYPE_NONE, LOG_TYPE_NONE, f"\nPyPercepthor Version: {version['name']}\n")
