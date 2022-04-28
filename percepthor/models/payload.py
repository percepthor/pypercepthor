import datetime
from pymongoose.mongo_types import Types, Schema

from models.payload import PAYLOAD_STATUS_NONE

class Payload (Schema):
	schema_name = "payloads"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},
			"configuration": {
				"type": Types.ObjectId,
				"ref": "submodules.configuration",
				"required": True
			},

			"token": {
				"type": Types.ObjectId,
				"ref": "tokens",
				"required": True
			},
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"required": True
			},

			"status": {
				"type": Types.Number,
				"default": PAYLOAD_STATUS_NONE
			},

			"props": {
				# we expect dynamic data
			},

			"data": {
				# we expect dynamic data
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Payload: {self.id}"
