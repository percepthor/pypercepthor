SERVICE_STATUS_NONE = 0
SERVICE_STATUS_CREATED = 1
SERVICE_STATUS_AVAILABLE = 2
SERVICE_STATUS_MAINTENANCE = 3
SERVICE_STATUS_DEPRECATED = 4
SERVICE_STATUS_REMOVED = 5

def service_status_to_string (status: int):
	result = "Undefined"

	if (status == SERVICE_STATUS_NONE):
		pass

	elif (status == SERVICE_STATUS_CREATED):
		result = "Created"

	elif (status == SERVICE_STATUS_AVAILABLE):
		result = "Available"

	elif (status == SERVICE_STATUS_MAINTENANCE):
		result = "Maintenance"

	elif (status == SERVICE_STATUS_DEPRECATED):
		result = "Deprecated"

	elif (status == SERVICE_STATUS_REMOVED):
		result = "Removed"

	return result
