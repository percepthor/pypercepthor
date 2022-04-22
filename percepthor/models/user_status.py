USER_STATUS_NONE = 0
USER_STATUS_ACTIVE = 1
USER_STATUS_INACTIVE = 2
USER_STATUS_BLOCKED = 3
USER_STATUS_REMOVED = 4

def user_status_to_string (status: int):
	result = "Undefined"

	if (status == USER_STATUS_NONE):
		pass

	elif (status == USER_STATUS_ACTIVE):
		result = "Active"

	elif (status == USER_STATUS_INACTIVE):
		result = "Inactive"

	elif (status == USER_STATUS_BLOCKED):
		result = "Blocked"

	elif (status == USER_STATUS_REMOVED):
		result = "Removed"

	return result
