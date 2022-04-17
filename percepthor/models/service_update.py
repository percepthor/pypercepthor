import datetime
from pymongoose.mongo_types import Types, Schema

from models.service_status import SERVICE_STATUS_NONE

class ServiceUpdate (Schema):
	schema_name = "services.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"default": None
			},

			"service_instance": {
				"type": Types.ObjectId,
				"ref": "services.instances",
				"default": None
			},

			"prev_status": {
				"type": Types.Number,
				"default": SERVICE_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": SERVICE_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ServiceUpdate: {self.id}"
