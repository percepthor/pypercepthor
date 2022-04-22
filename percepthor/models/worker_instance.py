import datetime
from pymongoose.mongo_types import Types, Schema

from models.worker_status import WORKER_INSTANCE_STATUS_NONE

WORKER_INSTANCE_TYPE_NONE = 0
WORKER_INSTANCE_TYPE_DEVELOPMENT = 1
WORKER_INSTANCE_TYPE_ADMIN = 2
WORKER_INSTANCE_TYPE_PRIORITY = 3
WORKER_INSTANCE_TYPE_COMMON = 4

def worker_instance_type_to_string (instance_type: int):
	result = "Undefined"

	if (instance_type == WORKER_INSTANCE_TYPE_NONE):
		pass

	elif (instance_type == WORKER_INSTANCE_TYPE_DEVELOPMENT):
		result = "Development"

	elif (instance_type == WORKER_INSTANCE_TYPE_ADMIN):
		result = "Admin"

	elif (instance_type == WORKER_INSTANCE_TYPE_PRIORITY):
		result = "Priority"

	elif (instance_type == WORKER_INSTANCE_TYPE_COMMON):
		result = "Common"

	return result

class WorkerInstance (Schema):
	schema_name = "workers.instances"

	def __init__ (self, **kwargs):
		self.schema = {
			"worker": {
				"type": Types.ObjectId,
				"ref": "workers",
				"required": True
			},

			"instance_type": {
				"type": Types.Number,
				"default": WORKER_INSTANCE_TYPE_NONE
			},

			"status": {
				"type": Types.Number,
				"default": WORKER_INSTANCE_STATUS_NONE
			},
			
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"default": None
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"WorkerInstance: {self.id}"
