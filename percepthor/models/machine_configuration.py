import datetime
from pymongoose.mongo_types import Types, Schema

class MachineConfiguration (Schema):
	schema_name = "machines.configuration"

	def __init__ (self, **kwargs):
		self.schema = {
			"machine": {
				"type": Types.ObjectId,
				"ref": "machines",
				"required": True
			},

			"platform": {
				"type": Types.String,
				"required": True
			},
			"series": {
				"type": Types.String,
				"required": True
			},
			"template": {
				"type": Types.String,
				"required": True
			},

			"cores": {
				"type": Types.Number,
				"default": 0
			},
			"memory": {
				"type": Types.Number,
				"default": 0
			},
			"gpus": {
				"gpu_type": {
					"type": Types.String,
					"required": True
				},
				"count": {
					"type": Types.Number,
					"default": 0
				}
			},

			"boot_disk": {
				"type": Types.ObjectId,
				"ref": "disks",
				"required": True
			},

			"disks": [{
				"type": Types.ObjectId,
				"ref": "disks",
				"required": False
			}],

			"networking": {
				"hostname": {
					"type": Types.String,
					"default": None
				},
				"internal": {
					"type": Types.String,
					"default": None
				},
				"external": {
					"type": Types.ObjectId,
					"ref": "networks",
					"default": None
				}
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"MachineConfiguration: {self.id}"
