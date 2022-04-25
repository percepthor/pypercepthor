import datetime
from pymongoose.mongo_types import Types, Schema

SUBMODULE_TYPE_NONE = 0
SUBMODULE_TYPE_CENSO = 1
SUBMODULE_TYPE_CENSO_CONTRASTED = 2
SUBMODULE_TYPE_TECHNIC_REPORT = 3
SUBMODULE_TYPE_QUIZZ = 4

def submodule_type_to_string (submodule_type: int):
	result = "Undefined"

	if (submodule_type == SUBMODULE_TYPE_NONE):
		pass

	elif (submodule_type == SUBMODULE_TYPE_CENSO):
		result = "Censo"

	elif (submodule_type == SUBMODULE_TYPE_CENSO_CONTRASTED):
		result = "Censo Contrasted"

	elif (submodule_type == SUBMODULE_TYPE_TECHNIC_REPORT):
		result = "Technic Report"

	elif (submodule_type == SUBMODULE_TYPE_QUIZZ):
		result = "Quizz"

	return result

SUBMODULE_PROCESS_NONE = 0
SUBMODULE_PROCESS_REAL = 1
SUBMODULE_PROCESS_WORK = 2

def submodule_process_to_string (process: int):
	result = "Undefined"

	if (process == SUBMODULE_PROCESS_NONE):
		pass

	elif (process == SUBMODULE_PROCESS_REAL):
		result = "Real"

	elif (process == SUBMODULE_PROCESS_WORK):
		result = "Work"

	return result

class Submodule (Schema):
	schema_name = "submodules"

	def __init__ (self, **kwargs):
		self.schema = {
			"module": {
				"type": Types.ObjectId,
				"ref": "modules",
				"required": True
			},

			"title": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"default": None
			},

			"s_type": {
				"type": Types.Number,
				"default": SUBMODULE_TYPE_NONE
			},
			"process": {
				"type": Types.Number,
				"default": SUBMODULE_PROCESS_NONE
			},

			"configuration": {
				"type": Types.ObjectId,
				"ref": "submodules.configuration",
				"default": None
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Submodule: {self.id}"
