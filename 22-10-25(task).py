#how to unpack the dictionary using while loop
print("How to unpack the dictionary using while loop")
dict = {"a": 1, "b": 2, "c": 3}
items = list(dict.items())
i = 0
while i < len(items):
    key, value = items[i]
    print(key,":",value)
    i += 1

print()

"""
lst = ['harsha', 'ranjth', 'kiran'] 
output: 
h 
a 
r 
s 
h 
a 
r 
a 
n 
j 
i 
t 
h 
k 
i 
r 
a 
n 
"""
lst = ['harsha', 'ranjth', 'kiran'] 
for ele in lst:
    for idx in range(len(ele)):
        print(ele[idx])
print()

#Adding zeroes to end
arr = [1,2,3,4,0,0,1,2,3,4,0,0,0,6]
new_arr = []

zero_count = arr.count(0)

for i in range(len(arr)):
    if arr[i]!=0:
        new_arr.append(arr[i])

for i in range(zero_count):
    new_arr.append(0)

print(arr)
print(new_arr) 


#bubblesort
print("Bubble Sort:")
lst = [64, 34, 25, 12, 22, 11, 90]
print("Before bubble sort: ",lst)
for i in range(len(lst)):
    for j in range(0, len(lst) - i - 1):
        if lst[j] > lst[j + 1]:
            lst[j], lst[j + 1] = lst[j + 1], lst[j]
print("After bubble sort: ",lst)
print()
