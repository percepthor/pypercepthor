import datetime
from pymongoose.mongo_types import Types, Schema

from models.service_status import SERVICE_STATUS_NONE

SERVICE_INSTANCE_TYPE_NONE = 0
SERVICE_INSTANCE_TYPE_LOCAL = 1
SERVICE_INSTANCE_TYPE_CLOUD = 2
SERVICE_INSTANCE_TYPE_OTHER = 3

def service_instance_type_to_string (instance_type: int):
	result = "Undefined"

	if (instance_type == SERVICE_INSTANCE_TYPE_NONE):
		pass

	elif (instance_type == SERVICE_INSTANCE_TYPE_LOCAL):
		result = "Local"

	elif (instance_type == SERVICE_INSTANCE_TYPE_CLOUD):
		result = "Cloud"

	elif (instance_type == SERVICE_INSTANCE_TYPE_OTHER):
		result = "Other"

	return result

class ServiceInstance (Schema):
	schema_name = "services.instances"

	def __init__ (self, **kwargs):
		self.schema = {
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"required": True
			},

			"instance_type": {
				"type": Types.Number,
				"default": SERVICE_INSTANCE_TYPE_NONE
			},
			"instance_idx": {
				"type": Types.Number,
				"required": True
			},

			"status": {
				"type": Types.Number,
				"default": SERVICE_STATUS_NONE
			},
			
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"default": None
			},

			"address": {
				"type": Types.String,
				"required": True
			},
			"weight": {
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
		return f"ServiceInstance: {self.id}"
