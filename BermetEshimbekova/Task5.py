# Task 4.5

def remember_result(f):
	result = None

	def wrapper(*args):
		nonlocal result
		print(f"Last result = ' {result}'")
		if all(isinstance(n, int) for n in args):
			result = 0
			for item in args:
				result += item
			print(f"Current result = '{result}'")
		else:
			result = f(*args)
	return wrapper


@remember_result
def sum_list(*args):
	result = ''
	for item in args:
		result += item
	print(f"Current result = '{result}'")
	return result


sum_list("a", "b")
sum_list("abc", "cde")
sum_list(3, 4, 5)
