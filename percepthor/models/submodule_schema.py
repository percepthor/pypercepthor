import datetime
from pymongoose.mongo_types import Types, Schema

class SubmoduleSchema (Schema):
	schema_name = "submodules.schema"

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
		return f"SubmoduleSchema: {self.id}"
