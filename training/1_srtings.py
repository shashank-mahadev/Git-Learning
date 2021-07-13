import string


#strings
print ("shashank")
name = 'Shashank Mahadev'
print (len(name))
print (name.upper())
print(name.count('ha'))
print (name.find("Mahadev")) # finds index
print (name.find("shamak")) # since not present it shows -1

message = "rule the world"
new_message = message.replace('world', "universe")
print(new_message + " and world")
print (name +' '+ new_message + "welcome")
sentance = "{} {}, welcome!".format(name, message) # string formatting
sentance_f = f"{name}, {message}, f-string!" # f-string can call with in place holder
sentance_f_1= f"{name.upper()},{message} f-string!" # f-string can even format

print (sentance)
print(sentance_f)
print(sentance_f_1)

print (dir(name)) # shows help for all the available attributes and methods
print (help(str)) # shows all the methods and what it does
print (help(str.lower)) # string is class and lower is method





