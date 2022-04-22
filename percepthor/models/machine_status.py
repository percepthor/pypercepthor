MACHINE_STATUS_NONE = 0
MACHINE_STATUS_CREATED = 1
MACHINE_STATUS_AVAILABLE = 2
MACHINE_STATUS_DOWN = 3
MACHINE_STATUS_MAINTENANCE = 4
MACHINE_STATUS_DEPRECATED = 5
MACHINE_STATUS_REMOVED = 6

def machine_status_to_string (status: int):
	result = "Undefined"

	if (status == MACHINE_STATUS_NONE):
		pass

	elif (status == MACHINE_STATUS_CREATED):
		result = "Created"

	elif (status == MACHINE_STATUS_AVAILABLE):
		result = "Available"

	elif (status == MACHINE_STATUS_DOWN):
		result = "Down"

	elif (status == MACHINE_STATUS_MAINTENANCE):
		result = "Maintenance"

	elif (status == MACHINE_STATUS_DEPRECATED):
		result = "Deprecated"

	elif (status == MACHINE_STATUS_REMOVED):
		result = "Removed"

	return result
