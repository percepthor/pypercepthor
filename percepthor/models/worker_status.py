WORKER_STATUS_NONE = 0
WORKER_STATUS_CREATED = 1
WORKER_STATUS_AVAILABLE = 2
WORKER_STATUS_MAINTENANCE = 3
WORKER_STATUS_DEPRECATED = 4
WORKER_STATUS_REMOVED = 5

def worker_status_to_string (status: int):
	result = "Undefined"

	if (status == WORKER_STATUS_NONE):
		pass

	elif (status == WORKER_STATUS_CREATED):
		result = "Created"

	elif (status == WORKER_STATUS_AVAILABLE):
		result = "Available"

	elif (status == WORKER_STATUS_MAINTENANCE):
		result = "Maintenance"

	elif (status == WORKER_STATUS_DEPRECATED):
		result = "Deprecated"

	elif (status == WORKER_STATUS_REMOVED):
		result = "Removed"

	return result

WORKER_INSTANCE_STATUS_NONE = 0
WORKER_INSTANCE_STATUS_AVAILABLE = 1
WORKER_INSTANCE_STATUS_WORKING = 2
WORKER_INSTANCE_STATUS_STOPPED = 3
WORKER_INSTANCE_STATUS_ENDED = 4
WORKER_INSTANCE_STATUS_MAINTENANCE = 5
WORKER_INSTANCE_STATUS_DEPRECATED = 6
WORKER_INSTANCE_STATUS_REMOVED = 7

def worker_instance_status_to_string (status: int):
	result = "Undefined"

	if (status == WORKER_INSTANCE_STATUS_NONE):
		pass

	elif (status == WORKER_INSTANCE_STATUS_AVAILABLE):
		result = "Available"

	elif (status == WORKER_INSTANCE_STATUS_WORKING):
		result = "Working"

	elif (status == WORKER_INSTANCE_STATUS_STOPPED):
		result = "Stopped"

	elif (status == WORKER_INSTANCE_STATUS_ENDED):
		result = "Ended"

	elif (status == WORKER_INSTANCE_STATUS_MAINTENANCE):
		result = "Maintenance"

	elif (status == WORKER_INSTANCE_STATUS_DEPRECATED):
		result = "Deprecated"

	elif (status == WORKER_INSTANCE_STATUS_REMOVED):
		result = "Removed"

	return result
