
# list comprehensions

nums = [1,2,3,4,5,6,7,8,9]

my_list=[]

for i in nums:
    my_list.append(i)
print(my_list)

# above same can be done in list comrehensions

my_list1=[n for n in nums]
print(my_list1)


for i in nums:
    my_list.append(i*i)
print(my_list)

my_list = [n*n for n in nums]

print(my_list)

