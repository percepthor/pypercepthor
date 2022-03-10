import datetime
from pymongoose.mongo_types import Types, Schema

TOKEN_STATUS_NONE = 0
TOKEN_STATUS_AVAILABLE = 1
TOKEN_STATUS_EXPIRED = 2
TOKEN_STATUS_DISABLED = 3
TOKEN_STATUS_REVOKED = 4

def token_status_to_string (status: int):
	result = "Undefined"

	if (status == TOKEN_STATUS_NONE):
		pass

	elif (status == TOKEN_STATUS_AVAILABLE):
		result = "Available"

	elif (status == TOKEN_STATUS_EXPIRED):
		result = "Expired"

	elif (status == TOKEN_STATUS_DISABLED):
		result = "Disabled"

	elif (status == TOKEN_STATUS_REVOKED):
		result = "Revoked"

	return result

TOKEN_TYPE_NONE = 0
TOKEN_TYPE_NORMAL = 1
TOKEN_TYPE_TEMPORARY = 2
TOKEN_TYPE_QUANTITY = 3

def token_type_to_string (status: int):
	result = "Undefined"

	if (status == TOKEN_TYPE_NONE):
		pass

	elif (status == TOKEN_TYPE_NORMAL):
		result = "Normal"

	elif (status == TOKEN_TYPE_TEMPORARY):
		result = "Temporary"

	elif (status == TOKEN_TYPE_QUANTITY):
		result = "Quantity"

	return result

class Token (Schema):
	schame_name = "tokens"

	def __init__ (self, **kwargs):
		self.schema = {
			"t_type": {
				"type": Types.Number,
				"default": TOKEN_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": TOKEN_STATUS_NONE
			},
			"user": {
				"type": Types.ObjectId,
				"ref": "users",
				"required": True
			},
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"default": None
			},
			"value": {
				"type": Types.String,
				"required": True
			},
			"data": {
				"type": Types.ObjectId,
				"ref": "tokens.data",
				"required": True
			},
			"permissions": {
				"type": Types.ObjectId,
				"ref": "permissions",
				"default": None
			},
			"created": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"expired": {
				"type": Types.Date,
				"default": None
			},
			"disabled": {
				"type": Types.Date,
				"default": None
			},
			"revoked": {
				"type": Types.Date,
				"default": None
			},
			
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"default": None
			},
			"mask": {
				"type": Types.Number,
				"default": 0
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Token: {self.id}"
