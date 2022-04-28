import datetime
from pymongoose.mongo_types import Types, Schema

class ServiceDocumentation (Schema):
	schema_name = "services.documentation"

	def __init__ (self, **kwargs):
		self.schema = self.schema = {
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"default": None
			},

			"filename": {
				"type": Types.String,
				"default": None
			},
			"sandbox": {
				"type": Types.Boolean,
				"default": False
			},
			
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ServiceDocumentation: {self.id}"
