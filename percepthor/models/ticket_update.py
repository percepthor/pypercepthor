import datetime
from pymongoose.mongo_types import Types, Schema

from models.ticket_status import TICKET_STATUS_NONE

class TicketUpdate (Schema):
	schema_name = "tickets.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"ticket": {
				"type": Types.ObjectId,
				"ref": "tickets",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": TICKET_STATUS_NONE
			},
			"current_status": {
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
