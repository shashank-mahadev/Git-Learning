
#Dictionaries

dict = {}
dict['one'] = "This is one"
dict[2]     = "This is two"

tinydict = {'name': 'john','code':6734, 'dept': 'sales'}


print (dict['one'] )      # Prints value for 'one' key
print (dict[2])           # Prints value for 2 key
print (tinydict)          # Prints complete dictionary
print (tinydict.keys())   # Prints all the keys
print (tinydict.values()) # Prints all the values




students = {'name' : "rama", 'age' : 26, 'skills' : ['archery', 'vedas', 'politics']}
print (students)
print(students["skills"])

# get method returns the values in more effecient ways instead of throwing the error

# print(students["phone"])
print(students.get("phone"))
print(students.get("phone", 'phone was outdated those days'))


# adding / updating the values

students["phone type"] = 'telepathy'
students['place'] = 'ayodhya'

print (students)


students.update({'name':'krishna', 'age':25})

print (students)


# delete

del students['age']

print (students)

# age = students.pop('age')
# print (students)
#
#
# print(age)


#loops

for key, value in students.items():
    print(key, value)




#### data frames ####


import pandas as pd

data1 = [1, 2, 3, 4, 5]
d1 = pd.DataFrame(data1)
print(d1)

fruits = {'fruit_name':['apple', 'orange', 'gauva'],'number':[9, 8, 7]}
f1 = pd.DataFrame(fruits)
print(f1)
