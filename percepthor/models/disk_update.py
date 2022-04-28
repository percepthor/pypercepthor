import datetime
from pymongoose.mongo_types import Types, Schema

from models.disk_status import DISK_STATUS_NONE

class DiskUpdate (Schema):
	schema_name = "disks.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"disk": {
				"type": Types.ObjectId,
				"ref": "disks",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": DISK_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": DISK_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Disk: {self.id}"
