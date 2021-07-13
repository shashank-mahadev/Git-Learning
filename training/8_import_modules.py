
courses = ['python', 'java', 'perl', 'c++', 'golang']

from shashank.functions7 import index_find

o1 = index_find(courses, 2)
print (o1)

import sys
from shashank.functions7 import index_find as aa
o1 = aa(courses, 3)
print (o1)

from shashank.functions7 import print_function, index_find
print(print_function())

from shashank.functions7 import *
print(print_function())

print(sys.path)
# "sys.path" prints the path of all the directories where python tries to import modules from

# if there are modules where the path is different than the current tree structure then we can add the path using "sys.path.append"
# example:
sys.path.append('/usr/local/shashank/*/******')




import random
print(random.choice(courses))

import math
rads = math.radians(90)
print(math.sin(rads))

import datetime
import calendar
today = datetime.date.today()
print(today)

is_leap = calendar.isleap(2021)
print(is_leap)

import os   # current working directory
print(os.getcwd())


print(os.__file__)


