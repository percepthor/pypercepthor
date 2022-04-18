import datetime
from pymongoose.mongo_types import Types, Schema

from models.service_status import SERVICE_STATUS_NONE

SERVICE_TYPE_NONE = 0
SERVICE_TYPE_CORE = 1
SERVICE_TYPE_RECON = 2
SERVICE_TYPE_WEB = 3
SERVICE_TYPE_EXTRA = 4

def service_type_to_string (service_type: int):
	result = "Undefined"

	if (service_type == SERVICE_TYPE_NONE):
		pass

	elif (service_type == SERVICE_TYPE_CORE):
		result = "Core"

	elif (service_type == SERVICE_TYPE_RECON):
		result = "Recon"

	elif (service_type == SERVICE_TYPE_WEB):
		result = "Web"

	elif (service_type == SERVICE_TYPE_EXTRA):
		result = "Extra"

	return result

class Service (Schema):
	schema_name = "services"

	def __init__ (self, **kwargs):
		self.schema = {
			"service_type": {
				"type": Types.Number,
				"default": SERVICE_TYPE_NONE
			},

			"status": {
				"type": Types.Number,
				"default": SERVICE_STATUS_NONE
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
			"next_value": {
				"type": Types.Number,
				"default": 0
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Service: {self.id}"
