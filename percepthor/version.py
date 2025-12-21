"""The versions of pypercepthor and of the libauth that it wraps."""

from cerver.utils import LOG_TYPE_NONE, cerver_log_both

from .lib import auth_function

__all__ = [
	"PERCEPTHOR_VERSION", "PERCEPTHOR_VERSION_NAME", "PERCEPTHOR_VERSION_DATE",
	"PERCEPTHOR_VERSION_TIME", "PERCEPTHOR_VERSION_AUTHOR",
	"version",
	"percepthor_libauth_version_print_full", "percepthor_libauth_version_print_version_id",
	"percepthor_libauth_version_print_version_name",
	"pypercepthor_version_print_full", "pypercepthor_version_print_version_id",
	"pypercepthor_version_print_version_name"
]

PERCEPTHOR_VERSION = "0.6.2"
PERCEPTHOR_VERSION_NAME = "Version 0.6.2"
PERCEPTHOR_VERSION_DATE = "21/11/2022"
PERCEPTHOR_VERSION_TIME = "10:01 CST"
PERCEPTHOR_VERSION_AUTHOR = "Erick Salas"

version = {
	"id": PERCEPTHOR_VERSION,
	"name": PERCEPTHOR_VERSION_NAME,
	"date": PERCEPTHOR_VERSION_DATE,
	"time": PERCEPTHOR_VERSION_TIME,
	"author": PERCEPTHOR_VERSION_AUTHOR
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
	"""Prints the version of pypercepthor with its date and its author."""
	output = (
		"\nPyPercepthor Version: {name}\n"
		"Release Date: {date} - {time}\n"
		"Author: {author}\n"
	).format (**version)

	cerver_log_both (LOG_TYPE_NONE, LOG_TYPE_NONE, output)

def pypercepthor_version_print_version_id () -> None:
	"""Prints the version id of pypercepthor."""
	cerver_log_both (LOG_TYPE_NONE, LOG_TYPE_NONE, f"\nPyPercepthor Version ID: {version['id']}\n")

def pypercepthor_version_print_version_name () -> None:
	"""Prints the version name of pypercepthor."""
	cerver_log_both (LOG_TYPE_NONE, LOG_TYPE_NONE, f"\nPyPercepthor Version: {version['name']}\n")
