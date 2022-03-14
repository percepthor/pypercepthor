from pymongoose.mongo_types import Types, Schema

class PermissionsAction (Schema):
	schema_name = "permissions.actions"

	def __init__ (self, **kwargs):
		self.schema = {
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"required": True
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"PermissionsAction: {self.id} - {self.name}"
