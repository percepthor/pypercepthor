import datetime
from pymongoose.mongo_types import Types, Schema

from models.machine_status import MACHINE_STATUS_NONE

class MachineUpdate (Schema):
	schema_name = "machines.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"machine": {
				"type": Types.ObjectId,
				"ref": "machines",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": MACHINE_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": MACHINE_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"MachineUpdate: {self.id}"
