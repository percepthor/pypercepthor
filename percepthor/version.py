from cerver.utils.log import LOG_TYPE_NONE, cerver_log_both

PERCEPTHOR_VERSION = "0.3"
PERCEPTHOR_VERSION_NAME = "Version 0.3"
PERCEPTHOR_VERSION_DATE = "22/04/2022"
PERCEPTHOR_VERSION_TIME = "08:09 CST"
PERCEPTHOR_VERSION_AUTHOR = "Erick Salas"

version = {
	"id": PERCEPTHOR_VERSION,
	"name": PERCEPTHOR_VERSION_NAME,
	"date": PERCEPTHOR_VERSION_DATE,
	"time": PERCEPTHOR_VERSION_TIME,
	"author": PERCEPTHOR_VERSION_AUTHOR
}

def pypercepthor_version_print_full ():
	output = "\nPyPercepthor Version: {name}\n" \
		"Release Date: {date} - {time}\n" \
		"Author: {author}\n".format (**version)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		output.encode ("utf-8")
	)

def pypercepthor_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyPercepthor Version ID: {version.id}\n".encode ("utf-8")
	)

def pypercepthor_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyPercepthor Version: {version.name}\n".encode ("utf-8")
	)
