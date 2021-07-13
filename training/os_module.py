

import os

print(dir(os))

print(os.getcwd())

#print(os.chdir("/shashank"))

print(os.listdir())

os.makedirs("shashank1")
#os.removedirs("shashank1")
os.rename("shashank1", "shashank2")
print(os.stat("shashank2").st_mtime)
# st_size

dir_structure = os.walk(os.getcwd()) # prints tree structure of the files
print (dir_structure)

file_path = os.path.join(os.environ.get('HOME'), 'test.txt')  # joins path

os.environ(os.getcwd())