# class is like a blueprint of the object
# when a function comes inside the class / associated with the class then we call it as "method"

#
#
# class Dog:
#     def __init__(self, name, kind, size):
#         self.name = name                  # "self.name" is attribute
#         self.kind = kind
#         self.size = size
#
#         print (f"{name} is a {kind} and is of {size} category")
#
#     def details(self, age, place):
#         self.age = age
#         self.place = place
#
#         print(f"age is {age} and born in {place}")
#
# a1 = Dog("Rocco", "hunting", "Big")   # a1 is the "instance" / "object"
# a2 = Dog("Dolly", "pet", "small")
#
# b1 = Dog.details(Dog, "3", "banglore")
# b2 = Dog.details(Dog, 7, "allappe")
#
#
#
#
# class Student:
#
#     def __init__(self, abc):
#         self.name = abc[0]
#         self.age = abc[1]
#         self.grade = abc[2]    # 0-100
#
#
#     def course(self):
#         course = ['sanskrit', 'english', 'politics']
#         if self.grade >= 85:
#             s1 = {self.name : [self.age,  self.grade, course[0]]}
#             return s1
#         elif self.grade == 50:
#             return course[1]
#         else:
#             return course[2]
#
#
#
#
#
# # new_list={Student.name : [Student.age, Student.grade, Student.course.coursee ]}
#
#
# s1=Student(["shashank", 34, 251])
# print(s1.course())
# s2=Student(["anil", 34, 30])
# print(s2.course())
# s3=Student(["malli", 38, 50])
# print(s3.course())
#
#
#
# # print (new_list)
#
# '''
# __init__  == initialise whenever a class is called, no need to call it explicitly
#
#
# '''
# print('starting new calss')
#
# class person:
#     def __init__(self, name):
#         self.name=name
#         print(name)
#
#     def details(self, age, height, profession):
#         self.age=age
#         self.height=height
#         self.profession=profession
#         print(f" is {self.age} years old and is of {self.height} ft and works as {self.profession} ")
#
# s1 = person("shashank")
# print(s1)
#
# s2 = s1.details( 34, 6, 'engg')
# print(s2)
#
#
# #### population count
#
# print ("start the population")
#
# class populationCount:
#
#     population = 0
#
#     def __init__(self, name):
#         self.name = name
#         populationCount.population += 1
#         print(f'howdy! you are a good addition {name}')
#         print(f'population is now {populationCount.population}')
#
#     def death(self):
#         print(f'its sad that we lost {self.name}')
#         populationCount.population -= 1
#         print(f'population is now {populationCount.population}')
#     def intro(self):
#
#         print(f'my name is {self.name}, nice to meet u all')
#
#     def count(self):
#         if populationCount.population == 1:
#             print('i am the last one')
#         else:
#             print(f'we are {populationCount.population} members left')
#
# person1 = populationCount('shashank')
# person1.count()
# person1.intro()
# # person1.death()
#
# person2 = populationCount('madhu')
#
# person2.count()
# person2.intro()
# person2.death()
#
# # print ("start the school")
# #
# # class mySchool():
# #     def __init__(self, name, age):
# #         self.name = name
# #         self.age = age
# #     def details(self):
# #         print(f'the members of the school are {self.name} and age is {self.age}')
# #
# # class students(mySchool):
# #     def __init__(self, name, age,  marks):
# #         mySchool.__init__(self, name, age)
# #         self.marks = marks
# #
# #     def details(self):
# #         print(f'the student name is {self.name} and age is {self.age} and the marks is {self.marks}')
# #
# # class teachers(mySchool):
# #     def __init__(self, name, age, salary):
# #         mySchool.__init__(self, name, age)
# #         self.salary = salary
# #     def details(self):
# #         print(f'the name of the teacher is {self.name} and age is {self.age} and the salary is {self.salary}')
# #
# #
# # s1=students('happy', 7, 97)
# # s2=students('viransh', 5, 85)
# #
# #
# # t1=teachers('shashank', 34, 97000000)
# # t2=teachers('anil', 34, 85000000)
# #
# # members = [s1, s2, t1, t2]
# # for i in members:
# #     i.details()
# #
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

class Dogs:
    def __init__(self, name, age):
        self.name = name
        self.age = age

        '''initializing dogs'''

    def details(self):
        '''initializing details'''
        print(f'dogs name is {self.name} and age is {self.age}')

class fight(Dogs):
    def __init__(self, name, age, fightclass):
        self.fightclass = fightclass
        Dogs.__init__(self, name, age)
    def details(self):
        Dogs.details(self)
        print(f'dog fight type is {self.fightclass}')

class pet(Dogs):
    def __init__(self, name, age, pettype):
        self.pettype = pettype

        Dogs.__init__(self, name, age)
    def details(self):
        Dogs.details(self)
        print(f'dog {self.age}pet type is {self.pettype}')


d1 = fight('rocco', 13, 'fight')
d2 = pet('jimmy', 5, 'pet')

member = [d1, d2]

for i in member:
    i.details()



d1.details()




###################### Using Files ##########################




