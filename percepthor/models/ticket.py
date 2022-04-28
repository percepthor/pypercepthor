import datetime
from pymongoose.mongo_types import Types, Schema

from models.ticket_status import TICKET_STATUS_NONE

TICKET_TYPE_NONE = 0
TICKET_TYPE_REPORT = 1
TICKET_TYPE_DISCOVER = 2

def ticket_type_to_string (t_type: int):
	result = "Undefined"

	if (t_type == TICKET_TYPE_NONE):
		pass

	elif (t_type == TICKET_TYPE_REPORT):
		result = "Report"

	elif (t_type == TICKET_TYPE_DISCOVER):
		result = "Discover"

	return result

class Ticket (Schema):
	schema_name = "tickets"

	def __init__ (self, **kwargs):
		self.schema = {
			"project": {
				"type": Types.ObjectId,
				"ref": "projects",
				"required": True
			},
			"name": {
				"type": Types.String,
				"default": None
			},
			"description": {
				"type": Types.String,
				"default": None
			},
			"image": {
				"type": Types.ObjectId,
				"ref": "images",
				"required": True
			},
			"t_type": {
				"type": Types.Number,
				"default": TICKET_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": TICKET_STATUS_NONE
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Ticket: {self.id}"
