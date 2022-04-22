import datetime
from pymongoose.mongo_types import Types, Schema

from models.worker_status import WORKER_STATUS_NONE

class WorkerUpdate (Schema):
	schema_name = "workers.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"worker": {
				"type": Types.ObjectId,
				"ref": "workers",
				"default": None
			},

			"worker_instance": {
				"type": Types.ObjectId,
				"ref": "workers.instances",
				"default": None
			},

			"prev_status": {
				"type": Types.Number,
				"default": WORKER_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": WORKER_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"WorkerUpdate: {self.id}"
