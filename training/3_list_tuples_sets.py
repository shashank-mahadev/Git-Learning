'''


Data structures

'''



# lists = []
# tuples = ()
# dict = {}


course = ['math', 'science', 'history', 'biology', 'chemistry']
codes = [25, 45, 67, 78, 98, 26, 74]

print (course[4])
print (codes[4])
print (course[:2])

print(min(codes))


# append, insert, extend, remove, pop, reverse, sort

course.append("arts")
print(course)

course.insert(1, 'sanskrit')
print(course)

course1 = ['politics', 'geometry']
course.insert(0, course1)
print(course)

course.extend(course1)
print(course)

course.remove('politics')
print(course)

# always pops/deletes last value
course.pop()
print(course)

popped_item = course.pop()
print(popped_item)
print(course)


course.reverse()
print(course)

course.pop()
course.sort()      # sorts alpabetically, if numbers then in ascending order
print(course)

# reverse it using "reverse=True"
course.sort(reverse=True)
print(course)


# check if item contains in the list usinh "in"
print("mechanics" in course)

# loop
for item in course:
    print(item)


# we can even give multiple inputs

# for index, item in course:
#     print(index, item)



# join and split

course_join = ' - '.join(course)
print (course_join)


course_split = course_join.split(' - ')
print (course_split)



######### TUPLES ###########
# tuples are immutable


subjects = ('math', 'science', 'history', 'biology', 'chemistry')
print(subjects)
# subjects[0] = 'kannada'  # this throws error as they cannot be modified

print(subjects)





########### SETS ################

# sets checks if the values is present or not, if there are any duplicate values it removes them
# intersection, difference, union

set1 = {'math', 'sanskrit', 'science', 'history', 'biology', 'chemistry', 'arts', 'politics', 'geometry', 'geometry'}
set2 = {'math', 'sanskrit', 'signals', 'thermodynamics', 'CAD', 'chemistry', 'CPP', 'politics', 'geometry', 'geometry'}

print(set1)


print('math' in set1)

print(set1.intersection(set2))
print(set1.difference(set2))
print(set1.union(set2))




############# create empty lists, tuples, set ##########

empty_list = []
empty_list = list()

empty_tuple = ()
empty_tuple = tuple()

empty_sets = {} # by doin this it create dict, hence use below
empty_sets = set()



'''
array : its the list with the same type
we can extend and shrink the array
'''

import array

vals = array()
