import datetime
from pymongoose.mongo_types import Types, Schema

class NetworkDomain (Schema):
	schema_name = "networks.domains"

	def __init__ (self, **kwargs):
		self.schema = {
			"network": {
				"type": Types.ObjectId,
				"ref": "networks",
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

			"address": {
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
		return f"NetworkDomain: {self.id}"
