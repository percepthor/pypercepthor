import datetime
from pymongoose.mongo_types import Types, Schema

from models.user_status import USER_STATUS_NONE

class UserUpdate (Schema):
	schema_name = "users.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"user": {
				"type": Types.ObjectId,
				"ref": "users",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": USER_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": USER_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"UserUpdate: {self.id}"
