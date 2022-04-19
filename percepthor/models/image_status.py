IMAGE_STATUS_NONE = 0
IMAGE_STATUS_AVAILABLE = 1
IMAGE_STATUS_LOST = 2
IMAGE_STATUS_IN_REVIEW = 3
IMAGE_STATUS_BLOCKED = 4
IMAGE_STATUS_MISSING = 5
IMAGE_STATUS_REMOVED = 6

def image_status_to_string (status: int):
	result = "Undefined"

	if (status == IMAGE_STATUS_NONE):
		pass

	elif (status == IMAGE_STATUS_AVAILABLE):
		result = "Available"

	elif (status == IMAGE_STATUS_LOST):
		result = "Lost"

	elif (status == IMAGE_STATUS_IN_REVIEW):
		result = "In Review"

	elif (status == IMAGE_STATUS_BLOCKED):
		result = "Blocked"

	elif (status == IMAGE_STATUS_MISSING):
		result = "Missing"

	elif (status == IMAGE_STATUS_REMOVED):
		result = "Removed"

	return result
