import datetime
from pymongoose.mongo_types import Types, Schema

from field_types import FIELD_TYPE_NONE

COMPONENT_CONFIG_TYPE_NONE = 0
COMPONENT_CONFIG_TYPE_CORE = 1
COMPONENT_CONFIG_TYPE_RECON = 2
COMPONENT_CONFIG_TYPE_CUSTOM = 3

COMPONENT_CONFIG_REQUEST_TYPE_NONE = 0
COMPONENT_CONFIG_REQUEST_TYPE_PAYLOAD = 1
COMPONENT_CONFIG_REQUEST_TYPE_LATEST = 2
COMPONENT_CONFIG_REQUEST_TYPE_CUSTOM = 3

COMPONENT_CONFIG_REQUIREMENT_NONE = 0
COMPONENT_CONFIG_REQUIREMENT_ALWAYS = 1
COMPONENT_CONFIG_REQUIREMENT_OPTIONAL = 2

COMPONENT_CONFIG_FIELD_OPTION_NONE = 0
COMPONENT_CONFIG_FIELD_OPTION_PAYLOAD = 1
COMPONENT_CONFIG_FIELD_OPTION_CUSTOM = 2

class ComponentConfiguration (Schema):
	schema_name = "modules.components.configuration"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},
			"component": {
				"type": Types.ObjectId,
				"ref": "components",
				"required": True
			},

			"config_type": {
				"type": Types.Number,
				"default": COMPONENT_CONFIG_TYPE_NONE
			},

			"services": [{
				"service_name": {
					"type": Types.String,
					"required": True
				},
				"request_type": {
					"type": Types.Number,
					"default": COMPONENT_CONFIG_REQUEST_TYPE_NONE
				},
				"depends_on": {
					"type": Types.String,
					"default": None
				},
				"conditions": [{
					"field": {
						"type": Types.String,
						"required": False
					},
					"field_type": {
						"type": Types.Number,
						"default": FIELD_TYPE_NONE
					},
					"value": {
						"default": None
					}
				}],
				"fields": [{
					"field_option": {
						"type": Types.Number,
						"default": COMPONENT_CONFIG_FIELD_OPTION_NONE
					},
					"name": {
						"type": Types.String,
						"required": False
					},
					"field": {
						"type": Types.String,
						"required": False
					},
					"value": {
						"required": False
					},
					"field_type": {
						"type": Types.Number,
						"default": FIELD_TYPE_NONE
					},
					"requirement": {
						"type": Types.Number,
						"default": COMPONENT_CONFIG_REQUIREMENT_NONE
					},
					"default_value": {
						"default": None
					}
				}]
			}],

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ComponentConfiguration: {self.id}"
