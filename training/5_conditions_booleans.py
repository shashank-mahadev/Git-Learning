
'''
Comparision
equal               ==
not equal           !=
greater than        >
lesser than         <
greater or equal    >=
lesser or equal     <=
object identity     is


and
or
not

### false values ##

false
none
Zero of any numeric type
Any empty sequence. ex, ()," ", []
any empty mapping. ex, {}


'''

# if-else

language = "python"

if language=='python':
    print("sure thing")
else:
    print("not necessary")


# else if

colour = "black"

if colour == "Red":
    print("colour is red")
elif colour == "white":
    print("color is white")
elif colour == "orange":
    print("color is orange")
else:
    print("no match")

#####################################

# when compared to "is" and "==" , 'is' will check if the object is stored in same memory, wher '==' will check the values

a = [1,2,3,4]
b = [1,2,3,4]

print (a == b)
print (a is b)

print(id(a)) # this will show that the id of these variables are stored in different location
print(id(b))



###############

condition = None
condition = False
condition = 0
condition = ''
condition = ()
condition = []
condition = {}

if condition:
    print("we choose true")
else:
    print ("we choose false ")


