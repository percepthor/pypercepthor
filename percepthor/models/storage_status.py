STORAGE_STATUS_NONE = 0
STORAGE_STATUS_AVAILABLE = 1
STORAGE_STATUS_DOWN = 2
STORAGE_STATUS_MAINTENANCE = 3
STORAGE_STATUS_DEPRECATED = 4
STORAGE_STATUS_REMOVED = 5

def storage_status_to_string (status: int):
	result = "Undefined"

	if (status == STORAGE_STATUS_NONE):
		pass

	elif (status == STORAGE_STATUS_AVAILABLE):
		result = "Available"

	elif (status == STORAGE_STATUS_DOWN):
		result = "Down"

	elif (status == STORAGE_STATUS_MAINTENANCE):
		result = "Maintenance"

	elif (status == STORAGE_STATUS_DEPRECATED):
		result = "Deprecated"

	elif (status == STORAGE_STATUS_REMOVED):
		result = "Removed"

	return result
