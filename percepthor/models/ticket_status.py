TICKET_STATUS_NONE = 0
TICKET_STATUS_CREATED = 1
TICKET_STATUS_WAITING = 2
TICKET_STATUS_IN_REVIEW = 3
TICKET_STATUS_GOOD = 4
TICKET_STATUS_BAD = 5
TICKET_STATUS_PASSED = 6
TICKET_STATUS_ERROR = 7

def ticket_status_to_string (status: int):
	result = "Undefined"

	if (status == TICKET_STATUS_NONE):
		pass

	elif (status == TICKET_STATUS_CREATED):
		result = "Created"

	elif (status == TICKET_STATUS_WAITING):
		result = "Waiting"

	elif (status == TICKET_STATUS_IN_REVIEW):
		result = "In Review"

	elif (status == TICKET_STATUS_GOOD):
		result = "Good"

	elif (status == TICKET_STATUS_BAD):
		result = "Bad"

	elif (status == TICKET_STATUS_PASSED):
		result = "Passed"

	elif (status == TICKET_STATUS_ERROR):
		result = "Error"

	return result
