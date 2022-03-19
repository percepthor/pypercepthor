import datetime
from pymongoose.mongo_types import Types, Schema

ACTION_TYPE_NONE = 0
ACTION_TYPE_PUSH = 1
ACTION_TYPE_ON_NEXT_SCREEN = 2
ACTION_TYPE_REQUETS = 3
ACTION_TYPE_ON_SUBMIT = 4
ACTION_TYPE_WHEN_COMPLETED = 5
ACTION_TYPE_EXIT = 6

def action_type_to_string (action_type: int):
	result = "Undefined"

	if (action_type == ACTION_TYPE_NONE):
		pass

	elif (action_type == ACTION_TYPE_PUSH):
		result = "Push"

	elif (action_type == ACTION_TYPE_ON_NEXT_SCREEN):
		result = "On Next Screen"

	elif (action_type == ACTION_TYPE_REQUETS):
		result = "Request"
	
	elif (action_type == ACTION_TYPE_ON_SUBMIT):
		result = "On Submit"

	elif (action_type == ACTION_TYPE_WHEN_COMPLETED):
		result = "When Completed"

	elif (action_type == ACTION_TYPE_EXIT):
		result = "Exit"

	return result

SCOPE_NONE = 0
SCOPE_LOCAL = 1
SCOPE_GLOBAL = 2

def scope_to_string (scope: int):
	result = "Undefined"

	if (scope == SCOPE_NONE):
		pass

	elif (scope == SCOPE_LOCAL):
		result = "Local"

	elif (scope == SCOPE_GLOBAL):
		result = "Global"

	return result

# TODO: request method types
REQUEST_METHOD_NONE = 0

class ComponentAction (Schema):
	schema_name = "components.actions"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"action_type": {
				"type": Types.Number,
				"default": ACTION_TYPE_NONE
			},
			"scope": {
				"type": Types.Number,
				"default": SCOPE_NONE
			},
			"screen": {
				"type": Types.String,
				"required": True
			},
			"route": {
				"type": Types.String,
				"required": True
			},
			"method": {
				"type": Types.Number,
				"default": REQUEST_METHOD_NONE
			},
			"args": {
				"type": Types.Number,
				"default": 0
			},
			"fields": {
				# we expect dynamic types
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ComponentAction: {self.id} - {self.user}"
