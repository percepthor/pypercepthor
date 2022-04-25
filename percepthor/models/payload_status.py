PAYLOAD_STATUS_NONE = 0
PAYLOAD_STATUS_CREATED = 1
PAYLOAD_STATUS_WAITING = 2
PAYLOAD_STATUS_PROCESSING = 3
PAYLOAD_STATUS_GOOD = 4
PAYLOAD_STATUS_BAD = 5
PAYLOAD_STATUS_FLAGGED = 6
PAYLOAD_STATUS_IN_REVIEW = 7
PAYLOAD_STATUS_PASSED = 8
PAYLOAD_STATUS_REMOVED = 9
PAYLOAD_STATUS_ERROR = 10

def payload_status_to_string (status: int):
	result = "Undefined"

	if (status == PAYLOAD_STATUS_NONE):
		pass

	elif (status == PAYLOAD_STATUS_CREATED):
		result = "Created"

	elif (status == PAYLOAD_STATUS_WAITING):
		result = "Waiting"

	elif (status == PAYLOAD_STATUS_PROCESSING):
		result = "Processing"

	elif (status == PAYLOAD_STATUS_GOOD):
		result = "Good"

	elif (status == PAYLOAD_STATUS_BAD):
		result = "Bad"

	elif (status == PAYLOAD_STATUS_FLAGGED):
		result = "Flagged"

	elif (status == PAYLOAD_STATUS_IN_REVIEW):
		result = "In Review"

	elif (status == PAYLOAD_STATUS_PASSED):
		result = "Passed"

	elif (status == PAYLOAD_STATUS_REMOVED):
		result = "Removed"

	elif (status == PAYLOAD_STATUS_ERROR):
		result = "Error"

	return result
