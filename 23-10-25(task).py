#Task-1

""" 
Optimize the below code:

def add_multiply(a,b):
    c = a + b # 15
    d = c * 2
    print(d)
    return d 


add_multiply(2,3)

def add_div(a,b):
    c  = a + b 
    e = c /2 
    print(e) """

""" #print()
print("Task-1")
print()

def add(num1,num2):
    return num1+num2

def add_multiply(add_val):
    return add_val*2
    

def add_div(add_val):
    return add_val/2

num1 = int(input("Enter 1st integer: "))
num2 = int(input("Enter 2nd integer: "))

add_val = add(num1,num2)

print("add_multiply: ", add_multiply(add_val))
print("add_division: ", add_div(add_val))

print() """
print("Task-2")
print()

def outer_func(num):
   #print("hi")
    def inner_func(a):
        print("hi")
        return 10 
    return inner_func

outer_func(20)