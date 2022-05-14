# Task 4.4
# Look through file `modules/legb.py`.

# 1) Find a way to call `inner_function` without moving it from inside of `enclosed_function`.
# call `inner_function` in `enclosed_function`.

# Is it enough to call `inner_function` in `enclosed_function`, right?


# 2.1) Modify ONE LINE in `inner_function` to make it print variable 'a' from global scope.

# global a # a = "I am local variable!"
# or
# print(globals()['a'])


# 2.2) Modify ONE LINE in `inner_function` to make it print variable 'a' form enclosing function.

# nonlocal a # a = "I am local variable!"
# or
# just comment line with local variable
import types

a = "I am global variable!"


def enclosing_funcion():
    a = "I am variable from enclosed function!"

    def inner_function():
        a = "I am local variable!"
        # global a    # a = "I am local variable!"
        # nonlocal a    # a = "I am local variable!"
        print(a)
        # print(globals()['a'])

    return inner_function()
