DISK_STATUS_NONE = 0
DISK_STATUS_CREATED = 1
DISK_STATUS_AVAILABLE = 2
DISK_STATUS_DOWN = 3
DISK_STATUS_DEPRECATED = 4
DISK_STATUS_REMOVED = 5

def disk_status_to_string (status: int):
	result = "Undefined"

	if (status == DISK_STATUS_NONE):
		pass

	elif (status == DISK_STATUS_CREATED):
		result = "Created"

	elif (status == DISK_STATUS_AVAILABLE):
		result = "Available"

	elif (status == DISK_STATUS_DOWN):
		result = "Down"

	elif (status == DISK_STATUS_DEPRECATED):
		result = "Deprecated"

	elif (status == DISK_STATUS_REMOVED):
		result = "Removed"

	return result
