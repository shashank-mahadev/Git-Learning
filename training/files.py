# f = open('test_file', 'r') # open files in read mode
# f.close() # close the file, Always close the files that u open
# print (f.name) # print name of file
#
#
#
# with open('test_file', 'r') as f: # using files like this is called context managers, its good practice. also this automatically closes the file within the manager
#     # print(f.read())
#     # print(f.readlines())
#     # print(f.readline())
#     # print(f.readlines(), end='')
#     print(f.read()) # reads 100 characters
#
# with open('test_file', 'w') as f: # using files like this is called context managers, its good practice. also this automatically closes the file within the manager
#     #print(f.write('this is a new line')) # this overwrites the files
#     print(f.seek)
#     print (f.write('shashank'))
#
# with open('test_file', 'a') as f: # to append the file
#     print(f.write(' mahadev'))
#     print(f.write('\n mahadev'))
#
#


####

f = open('text.txt', 'r')
with open('text.txt', 'r') as f:
    # contents = f.readline()
    # print(contents, end='')
    #
    # for line in f:
    #     print(line, end='')

    contents = f.read(100) # prints 100 characters
    print (contents)

    contents = f.read(100)  # now this block prints 100 charac ters after the the above block
    print(contents)

    contents = f.seek(0) # this will reset the position of the cursor to the start

    contents = f.read(100)  # now this block prints 100 charac ters after the the above block
    print(contents)



with open('text1.txt', 'w') as f:
    f.write('test')                 # writes the data to the file, if file doesnt it creates one

    f.write(' Shashank')
    f.seek(0)                          # rewrite the characters starting from 0
    f.write(' Mahadev')










