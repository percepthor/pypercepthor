import datetime
from pymongoose.mongo_types import Types, Schema

class ServiceRoute (Schema):
	schema_name = "services.routes"

	def __init__ (self, **kwargs):
		self.schema = self.schema = {
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"default": None
			},

			"documentation": {
				"type": Types.ObjectId,
				"ref": "services.documentation",
				"default": None
			},

			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"required": True
			},
			"path": {
				"type": Types.String,
				"required": True
			},

			"fields": [{
				"name": {
					"type": Types.String,
					"required": True
				},
				"field_type": {
					"type": Types.Number,
					"default": 0
				},
				"requirement": {
					"type": Types.Number,
					"default": 0
				},
				"default_value": {
					"type": Types.String,
					"default": None
				}
			}],

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ServiceRoute: {self.id}"
