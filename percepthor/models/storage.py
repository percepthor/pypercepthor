import datetime
from pymongoose.mongo_types import Types, Schema

from models.storage_status import STORAGE_STATUS_NONE

STORAGE_TYPE_NONE = 0
STORAGE_TYPE_LOCAL = 1
STORAGE_TYPE_CLOUD = 2
STORAGE_TYPE_BUCKET = 3

def storage_type_to_string (storage_type: int):
	result = "Undefined"

	if (storage_type == STORAGE_TYPE_NONE):
		pass

	elif (storage_type == STORAGE_TYPE_LOCAL):
		result = "Available"

	elif (storage_type == STORAGE_TYPE_CLOUD):
		result = "Maintenance"

	elif (storage_type == STORAGE_TYPE_BUCKET):
		result = "Bucket"

	return result

STORAGE_GOAL_NONE = 0
STORAGE_GOAL_GENERAL = 1
STORAGE_GOAL_UPLOADS = 2
STORAGE_GOAL_OUTPUT = 3
STORAGE_GOAL_RECON = 4
STORAGE_GOAL_BACKUP = 5
STORAGE_GOAL_TEMP = 6
STORAGE_GOAL_CACHE = 7

def storage_goal_to_string (goal: int):
	result = "Undefined"

	if (goal == STORAGE_GOAL_NONE):
		pass

	elif (goal == STORAGE_GOAL_GENERAL):
		result = "General"

	elif (goal == STORAGE_GOAL_UPLOADS):
		result = "Uploads"

	elif (goal == STORAGE_GOAL_OUTPUT):
		result = "Output"

	elif (goal == STORAGE_GOAL_RECON):
		result = "Recon"

	elif (goal == STORAGE_GOAL_BACKUP):
		result = "Backup"

	elif (goal == STORAGE_GOAL_TEMP):
		result = "Temp"

	elif (goal == STORAGE_GOAL_CACHE):
		result = "Cache"

	return result

STORAGE_SCOPE_NONE = 0
STORAGE_SCOPE_GENERAL = 1
STORAGE_SCOPE_SERVICE = 2
STORAGE_SCOPE_ORGANIZATION = 3
STORAGE_SCOPE_PROJECT = 4

def storage_scope_to_string (scope: int):
	result = "Undefined"

	if (scope == STORAGE_SCOPE_NONE):
		pass

	elif (scope == STORAGE_SCOPE_GENERAL):
		result = "General"

	elif (scope == STORAGE_SCOPE_SERVICE):
		result = "Service"

	elif (scope == STORAGE_SCOPE_ORGANIZATION):
		result = "Organization"

	elif (scope == STORAGE_SCOPE_PROJECT):
		result = "Project"

	return result

class Storage (Schema):
	schema_name = "storages"

	def __init__ (self, **kwargs):
		self.schema = {
			"machine": {
				"type": Types.ObjectId,
				"ref": "machines",
				"required": True
			},

			"storage_type": {
				"type": Types.Number,
				"default": STORAGE_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": STORAGE_STATUS_NONE
			},
			"goal": {
				"type": Types.Number,
				"default": STORAGE_GOAL_NONE
			},

			"alias": {
				"type": Types.String,
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

			"scope": {
				"type": Types.Number,
				"default": STORAGE_SCOPE_NONE
			},
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"default": None
			},
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"default": None
			},
			"project": {
				"type": Types.ObjectId,
				"ref": "projects",
				"default": None
			},

			"path": {
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
		return f"Storage: {self.id}"
