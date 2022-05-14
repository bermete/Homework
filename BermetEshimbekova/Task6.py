# Task 4.6

def call_once(f):
    result = 0

    def wrapper(*args):
        nonlocal result
        if not result:
            result = f(*args)
        return result
    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b


print(sum_of_numbers(13, 42))
print(sum_of_numbers(999, 100))
print(sum_of_numbers(134, 412))
print(sum_of_numbers(856, 232))
