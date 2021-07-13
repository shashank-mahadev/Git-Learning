cars = {'name': 'jaguar', 'speed': 200}
list = ["hummer", 180]

print (" My car is {} that runs at the speed of {} km".format(cars['name'], cars['speed']))

print (" My car is {0} that runs at the speed of {1} km".format(cars['name'], cars['speed']))

statement ="My car is {0[name]} the speed is {0[speed]}".format(cars)
print(statement)


# f strings
sentance = f"My car is {cars['name']} and speed is {cars['speed']}"
print(sentance)

print (f"my car is {list[0]} and speed is {list[1]}")


