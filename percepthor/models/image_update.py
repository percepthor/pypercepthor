import datetime
from pymongoose.mongo_types import Types, Schema

from models.image_status import IMAGE_STATUS_NONE

class ImageUpdate (Schema):
	schema_name = "images.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"image": {
				"type": Types.ObjectId,
				"ref": "images",
				"default": None
			},

			"prev_status": {
				"type": Types.Number,
				"default": IMAGE_STATUS_NONE
			},
			"current_status": {
				"type": Types.Number,
				"default": IMAGE_STATUS_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ImageUpdate: {self.id}"
