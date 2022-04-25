import datetime
from pymongoose.mongo_types import Types, Schema

NETWORK_TYPE_NONE = 0
NETWORK_TYPE_LOCAL = 1
NETWORK_TYPE_CLOUD = 2

def network_type_to_string (network_type: int):
	result = "Undefined"

	if (network_type == NETWORK_TYPE_NONE):
		pass

	elif (network_type == NETWORK_TYPE_LOCAL):
		result = "Local"

	elif (network_type == NETWORK_TYPE_CLOUD):
		result = "Cloud"

	return result

NETWORK_TIER_NONE = 0
NETWORK_TIER_STANDARD = 1
NETWORK_TIER_PREMIUM = 2

def network_tier_to_string (tier: int):
	result = "Undefined"

	if (tier == NETWORK_TIER_NONE):
		pass

	elif (tier == NETWORK_TIER_STANDARD):
		result = "Standard"

	elif (tier == NETWORK_TIER_PREMIUM):
		result = "Premium"

	return result

class Network (Schema):
	schema_name = "networks"

	def __init__ (self, **kwargs):
		self.schema = {
			"network_type": {
				"type": Types.Number,
				"default": NETWORK_TYPE_NONE
			},

			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"required": True
			},

			"address": {
				"type": Types.String,
				"required": True
			},

			"region": {
				"type": Types.String,
				"default": None
			},

			"tier": {
				"type": Types.Number,
				"default": NETWORK_TIER_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Network: {self.id}"
