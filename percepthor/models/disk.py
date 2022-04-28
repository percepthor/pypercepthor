import datetime
from pymongoose.mongo_types import Types, Schema

from models.disk_status import DISK_STATUS_NONE

DISK_TYPE_NONE = 0
DISK_TYPE_STANDARD = 1
DISK_TYPE_BALANCED = 2
DISK_TYPE_SSD = 3
DISK_TYPE_EXTREME = 4

def disk_type_to_string (disk_type: int):
	result = "Undefined"

	if (disk_type == DISK_TYPE_NONE):
		pass

	elif (disk_type == DISK_TYPE_STANDARD):
		result = "Standard"

	elif (disk_type == DISK_TYPE_BALANCED):
		result = "Balanced"

	elif (disk_type == DISK_TYPE_SSD):
		result = "SSD"

	elif (disk_type == DISK_TYPE_EXTREME):
		result = "Extreme"

	return result

class Disk (Schema):
	schema_name = "disks"

	def __init__ (self, **kwargs):
		self.schema = {
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"default": None
			},

			"status": {
				"type": Types.Number,
				"default": DISK_STATUS_NONE
			},
			"disk_type": {
				"type": Types.Number,
				"default": DISK_TYPE_NONE
			},

			"image": {
				"type": Types.String,
				"default": None
			},
			"size": {
				"type": Types.Number,
				"default": 0
			},
			"device_name": {
				"type": Types.String,
				"default": None
			},

			"path": {
				"type": Types.String,
				"required": True
			},
			"format": {
				"type": Types.String,
				"required": True
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Disk: {self.id}"
