

def empty_function():
    pass  # passes function without throwing error if there is nothing inside the function


def print_function():
    print("Hello baby")


#print_function()




# In case your function needs input arguments

#                     _____ this is mandatory argument that needs to be passed while using the function
#                    |      this is also called formal argument
#                    |
def my_function(greeting, comments):

    return f'{greeting} shashank! and they say {comments} '



print (my_function('welcome', 'goodbye'))      # here 'welcome' and 'goodbye' are called as actual/ position arguments
print (len(my_function('welcome', 'goodbye')))

print(my_function('howdy', 'good lad').upper())

print(my_function('hi', "fuck off"))

# if you need a default value to be assigned when no arguments is passed. assign value while defining function

def car_function(name="BMW", type='luxuary'):
    return f"my car is {name} and it is a {type} car"

print(car_function())
print(car_function('ferrari', 'sports'))




# variable length arguments and keyword variable length arguments
# here u can pass any number of arguments at
# '*' - will always store in tuple
# '**' - will always store in dict


def family_function(*args, **kwargs):
    # return f"myfamily members are {args} and their age and place is {kwargs}"
    # print(family_function())
    print(args)
    print(kwargs)

family_function('mahadev', 'shylaja', 'shashank', 'sindhu', 'aarya', age='64', place='bangalore', gender='male' )
family_function('shank', 'sindhu', salary='20000000', respnsibility='family')

# we can also pass list and dict

def bike_function(*args, **kwargs):

    print(args)
    print(kwargs)

types = ['cross', 'sports', 'cruiser', 'urban']
details = {'himalayan' :'royal enfield', 'CBR' : 'honda', 'iron800' : 'Harley dacvison', 'r125' : 'aprilla'}

bike_function(*types, **details)



def index_find(list, index):
    print(list[index])





