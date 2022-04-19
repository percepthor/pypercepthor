import datetime
from pymongoose.mongo_types import Types, Schema

from models.storage_status import STORAGE_STATUS_NONE

class StorageUpdate (Schema):
	schema_name = "storages.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"storage": {
				"type": Types.ObjectId,
				"ref": "storages",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": STORAGE_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": STORAGE_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"StorageUpdate: {self.id}"
