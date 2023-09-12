def construct_errors_msg(errors: dict):
	if errors is None:
		return None

	result = []
	for k, v in errors.items():
		error = v.pop()
		result.append(error.message)

	return result
