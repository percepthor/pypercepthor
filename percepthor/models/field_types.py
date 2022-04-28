FIELD_TYPE_NONE = 0
FIELD_TYPE_NUMBER = 1
FIELD_TYPE_STRING = 2
FIELD_TYPE_BOOL = 3
FIELD_TYPE_PHOTO = 4
FIELD_TYPE_ITEM = 5
FIELD_TYPE_ITEM_LIST = 6
FIELD_TYPE_NUMBER_LIST = 7
FIELD_TYPE_STRING_LIST = 8
FIELD_TYPE_DICT_LIST = 9

def field_type_to_string (field_type: int):
	result = "Undefined"

	if (field_type == FIELD_TYPE_NONE):
		pass

	elif (field_type == FIELD_TYPE_NUMBER):
		result = "Number"

	elif (field_type == FIELD_TYPE_STRING):
		result = "String"

	elif (field_type == FIELD_TYPE_BOOL):
		result = "Bool"

	elif (field_type == FIELD_TYPE_PHOTO):
		result = "Photo"

	elif (field_type == FIELD_TYPE_ITEM):
		result = "Item"

	elif (field_type == FIELD_TYPE_ITEM_LIST):
		result = "Item List"

	elif (field_type == FIELD_TYPE_NUMBER_LIST):
		result = "Number List"

	elif (field_type == FIELD_TYPE_STRING_LIST):
		result = "String List"

	elif (field_type == FIELD_TYPE_DICT_LIST):
		result = "Dict List"
	
	return result
