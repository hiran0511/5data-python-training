print("Multiple Decorators Example:")
print()
def decorator_A(func):
    def wrapper():
        print("Start A")
        func()
        print("End A")
    return wrapper

def decorator_B(func):
    def wrapper():
        print("Start B")
        func()
        print("End B")
    return wrapper

@decorator_A
@decorator_B
def greet():
    print("Hello!")

greet()

""" 
step-by-step breakdown:

1. decorator_B wraps greet
2. decorator_A wraps the result of decorator_B
3. greet is replaced with the wrapper returned by decorator_A
4. greet() calls the outer wrapper (from decorator_A)
5. inside wrapper_A: prints "Start A"
6. wrapper_A calls func(), which is wrapper_B
7. inside wrapper_B: prints "Start B"
8. wrapper_B calls the original greet() -> prints "Hello!"
9. wrapper_B prints "End B"
10. control returns to wrapper_A, which prints "End A"

In simpler terms:

- decorator_B wraps the original function first.
- decorator_A then wraps decorator_B’s result.
- When greet() is called:
  → decorator_A runs first (outermost)
  → it calls decorator_B (next layer)
  → decorator_B calls the original function greet().


-> In the execution flow why decorator_B is called?

@decorator_A
@decorator_B
def greet():
    print("Hello!")

It's equivalent to:

greet = decorator_A(decorator_B(greet))

So first decorator_B is called whose result is wrapped by decorator_A.

-> Why func() line present in decorators

When you use multiple decorators, each decorator's wrapper function can call the next decorator's 
wrapper function (or the original function) using func().

If you don't include func() in a decorator's wrapper function, it will stop the chain of decorators, 
and any decorators applied after it won't be executed.
"""
