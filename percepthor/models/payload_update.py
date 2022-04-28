import datetime
from pymongoose.mongo_types import Types, Schema

from models.payload_status import PAYLOAD_STATUS_NONE

class PayloadUpdate (Schema):
	schema_name = "payloads.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"payload": {
				"type": Types.ObjectId,
				"ref": "payloads",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": PAYLOAD_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": PAYLOAD_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Payload: {self.id}"
