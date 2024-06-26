def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper


@my_decorator
def say_hello():
    print('Hello')
    return 2 * 4  # for some reason, fn being decorated does not return its contents

print(say_hello())
