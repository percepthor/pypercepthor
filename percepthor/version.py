from cerver.utils.log import LOG_TYPE_NONE, cerver_log_both

from .lib import lib

PYPERCEPTHOR_VERSION = "0.1".encode ('utf-8')
PYPERCEPTHOR_VERSION_NAME = "Version 0.1".encode ('utf-8')
PYPERCEPTHOR_VERSION_DATE = "12/07/2021".encode ('utf-8')
PYPERCEPTHOR_VERSION_TIME = "09:54 CST".encode ('utf-8')
PYPERCEPTHOR_VERSION_AUTHOR = "Erick Salas".encode ('utf-8')

percepthor_libauth_version_print_full = lib.percepthor_libauth_version_print_full
percepthor_libauth_version_print_version_id = lib.percepthor_libauth_version_print_version_id
percepthor_libauth_version_print_version_name = lib.percepthor_libauth_version_print_version_name

def pypercepthor_version_print_full ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nPyPercepthor Version: %s".encode ('utf-8'), PYPERCEPTHOR_VERSION_NAME
	)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"Release Date & time: %s - %s".encode ('utf-8'),
		PYPERCEPTHOR_VERSION_DATE, PYPERCEPTHOR_VERSION_TIME
	)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"Author: %s\n".encode ('utf-8'),
		PYPERCEPTHOR_VERSION_AUTHOR
	)

def pypercepthor_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nPyPercepthor Version ID: %s\n".encode ('utf-8'),
		PYPERCEPTHOR_VERSION
	)

def pypercepthor_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nPyPercepthor Version: %s\n".encode ('utf-8'),
		PYPERCEPTHOR_VERSION_NAME
	)
