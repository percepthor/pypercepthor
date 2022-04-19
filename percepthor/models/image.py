import datetime
from pymongoose.mongo_types import Types, Schema

from models.image_status import IMAGE_STATUS_NONE

IMAGE_TYPE_NONE = 0
IMAGE_TYPE_COMMON = 1
IMAGE_TYPE_UPLOAD = 2
IMAGE_TYPE_OUTPUT = 3
IMAGE_TYPE_BACKUP = 4

def image_type_to_string (image_type: int):
	result = "Undefined"

	if (image_type == IMAGE_TYPE_NONE):
		pass

	elif (image_type == IMAGE_TYPE_COMMON):
		result = "Common"

	elif (image_type == IMAGE_TYPE_UPLOAD):
		result = "Upload"

	elif (image_type == IMAGE_TYPE_OUTPUT):
		result = "Output"

	elif (image_type == IMAGE_TYPE_BACKUP):
		result = "Backup"

	return result

class Image (Schema):
	schema_name = "images"

	def __init__ (self, **kwargs):
		self.schema = {
			"storage": {
				"type": Types.ObjectId,
				"ref": "storages",
				"default": None
			},

			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"default": None
			},

			"image_type": {
				"type": Types.Number,
				"default": IMAGE_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": IMAGE_STATUS_NONE
			},

			"filename": {
				"type": Types.String,
				"required": True
			},
			
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Image: {self.id}"
