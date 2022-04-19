import datetime
from pymongoose.mongo_types import Types, Schema

from models.worker_status import WORKER_STATUS_NONE

WORKER_TYPE_NONE = 0
WORKER_TYPE_CORE = 1
WORKER_TYPE_RECON = 2
WORKER_TYPE_WEB = 3
WORKER_TYPE_OTHER = 4

def worker_type_to_string (worker_type: int):
	result = "Undefined"

	if (worker_type == WORKER_TYPE_NONE):
		pass

	elif (worker_type == WORKER_TYPE_CORE):
		result = "Core"

	elif (worker_type == WORKER_TYPE_RECON):
		result = "Recon"

	elif (worker_type == WORKER_TYPE_WEB):
		result = "Web"

	elif (worker_type == WORKER_TYPE_OTHER):
		result = "Other"

	return result

class Worker (Schema):
	schema_name = "workers"

	def __init__ (self, **kwargs):
		self.schema = {
			"worker_type": {
				"type": Types.Number,
				"default": WORKER_TYPE_NONE
			},

			"status": {
				"type": Types.Number,
				"default": WORKER_STATUS_NONE
			},

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
				"required": True
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Worker: {self.id}"
