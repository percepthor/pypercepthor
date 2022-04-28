import datetime
from pymongoose.mongo_types import Types, Schema

from models.field_types import FIELD_TYPE_NONE

COMPONENT_TYPE_NONE = 0
COMPONENT_TYPE_PHOTO = 1
COMPONENT_TYPE_COUNTER = 2
COMPONENT_TYPE_OPEN_ANSWER = 3
COMPONENT_TYPE_MULTIPLE_CHOICE_ANSWER = 4
COMPONENT_TYPE_ACTION_BUTTON = 5
COMPONENT_TYPE_LIST_PHOTO = 6

def component_type_to_string (component_type: int):
	result = "Undefined"

	if (component_type == COMPONENT_TYPE_NONE):
		pass

	elif (component_type == COMPONENT_TYPE_PHOTO):
		result = "Photo"

	elif (component_type == COMPONENT_TYPE_COUNTER):
		result = "Counter"

	elif (component_type == COMPONENT_TYPE_OPEN_ANSWER):
		result = "Open Answer"

	elif (component_type == COMPONENT_TYPE_MULTIPLE_CHOICE_ANSWER):
		result = "Multiple Choise Answer"
	
	elif (component_type == COMPONENT_TYPE_ACTION_BUTTON):
		result = "Action Button"

	elif (component_type == COMPONENT_TYPE_LIST_PHOTO):
		result = "List Photo"

	return result

BUTTON_TYPE_NONE = 0
BUTTON_TYPE_TEXT = 1
BUTTON_TYPE_ELEVATED = 2

def button_type_to_string (button_type: int):
	result = "Undefined"

	if (button_type == BUTTON_TYPE_NONE):
		pass

	elif (button_type == BUTTON_TYPE_TEXT):
		result = "Text"

	elif (button_type == BUTTON_TYPE_ELEVATED):
		result = "Elevated"

	return result

class Component (Schema):
	schema_name = "modules.components"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"screen": {
				"type": Types.ObjectId,
				"ref": "modules.screens"
			},

			"component_type": {
				"type": Types.Number,
				"default": COMPONENT_TYPE_NONE
			},

			"index": {
				"type": Types.Number,
				"required": True
			},
			
			"name": {
				"type": Types.String,
				"required": True
			},
			"label": {
				"type": Types.String,
				"required": True
			},
			"field_name": {
				"type": Types.String,
				"required": True
			},
			"default_value": {
				"default": None
			},
			"options": [{
				"type": Types.String,
				"required": False
			}],
			"selectable": {
				"type": Types.Number,
				"default": 0
			},

			"button_type": {
				"type": Types.Number,
				"default": BUTTON_TYPE_NONE
			},
			"item_name": {
				"type": Types.String,
				"default": None
			},
			"field_type": {
				"type": Types.Number,
				"default": FIELD_TYPE_NONE
			},

			"photo_types": {
				"type": Types.ObjectId,
				"ref": "modules.photo.types",
				"default": None
			},

			"children": [{
				"type": Types.ObjectId,
				"ref": "modules.components",
				"required": False
			}],

			"restrictions": [{
				"type": Types.ObjectId,
				"ref": "modules.restrictions",
				"required": False
			}],

			"conditions": [{
				"type": Types.ObjectId,
				"ref": "modules.conditions",
				"required": False
			}],

			"color": {
				"type": Types.String,
				"default": None
			},

			"actions": [{
				"type": Types.ObjectId,
				"ref": "modules.components.actions",
				"required": False
			}],

			"max_internal_items": {
				"type": Types.Number,
				"default": 0
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Component: {self.id}"
