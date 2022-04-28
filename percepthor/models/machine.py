import datetime
from pymongoose.mongo_types import Types, Schema

from models.machine_status import MACHINE_STATUS_NONE

MACHINE_TYPE_NONE = 0
MACHINE_TYPE_LOCAL = 1
MACHINE_TYPE_CLOUD = 2

def machine_type_to_string (machine_type: int):
	result = "Undefined"

	if (machine_type == MACHINE_TYPE_NONE):
		pass

	elif (machine_type == MACHINE_TYPE_LOCAL):
		result = "Local"

	elif (machine_type == MACHINE_TYPE_CLOUD):
		result = "Cloud"

	return result

class Machine (Schema):
	schema_name = "machines"

	def __init__ (self, **kwargs):
		self.schema = {
			"alias": {
				"type": Types.String,
				"required": True
			},
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"default": None
			},

			"machine_type": {
				"type": Types.Number,
				"default": MACHINE_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": MACHINE_STATUS_NONE
			},

			"region": {
				"type": Types.String,
				"default": None
			},
			"zone": {
				"type": Types.String,
				"default": None
			},

			"configuration": {
				"type": Types.ObjectId,
				"ref": "machines.configuration",
				"default": None
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Machine: {self.id}"
