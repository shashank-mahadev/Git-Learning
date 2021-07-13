# variable types
# 1. Instance variable
# 2. Class variable / static variables


class super_heros:

    power = "strength"  # class variable/static variable, if changed it effects all objects, this comes under class

    def __init__(self):
        self.thor = "hammer"         # instance variables, because this can be changed
        self.ironman = "technology"   # instance variables, because this can be changed


hero_1 = super_heros() # objects
hero_2 = super_heros() # objects

print(hero_1.thor, hero_1.ironman)

hero_1.ironman="suit"
hero_2.thor="axe"

print(hero_1.ironman, hero_2.thor)
print(hero_1.thor, hero_2.ironman, hero_2.power)

super_heros.power="reliance"

print(hero_1.thor, hero_2.ironman, hero_2.power)


# variables scoping
# common abbreviations " LEGB " --> " Local, Enclosing, , Builtin "

x = 'global x'  # global variable

def test():
    y = 'local y' # local variable
    x = 'changed'
    print(y)
    print(x)

test()


def test2():
    a = 'local a'
    print(a)
    # x = 'change2'
    # print(y) # this cannot be called as its local to the function
    print(x)
test2()



# built-in scope -----> these are built functions in python

import builtins
print (dir(builtins))


m = max([1, 2, 3, 4, 5] )

print(m)


# Enclosing variable

def outer():
    x = 'outer x'

    def inner():
        x = 'inner x'
        print(x)
    inner()

    #print(x)

outer()

