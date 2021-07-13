#
# # 1. Write a program to reverse a string
# def str_reverse(string):
#     r_string = string[::-1]
#     print(r_string)
#
# string = 'abcd'
# str_reverse(string)
#
# ########################################################################################################
#
# # 2. Write a program to find and replace excellent in string “Anil plays excellent cricket”
# def replace_string(sentance, replaceble, replaced):
#     new_sentance = sentance.replace(replaceble, replaced)
#     print(new_sentance)
#
# sentance = "Anil plays excellent cricket"
# replaceble = "excellent"
# replaced = "good"
# print (replace_string(sentance, replaceble, replaced))
#
#
# ########################################################################################################
#
# # 3. Create a list of strings and use append and extend methods
#
#
#
#
#
# ########################################################################################################
#
# # 4. Create a list of numbers from 1 to 10 and check for number 8 and and remove this number
# def sort_list(my_list, remove_item):
#     my_list.remove(remove_item)
#
# my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# sort_list(my_list, 5)
# print(my_list)
#
#
# ########################################################################################################
#
# # 6. [“ab”, “cd” “ef”, “gh”, “ij”, “kl”, “mn”] print one if element is ab, print two if the element is cd, print three if element is kl and print four in all other conditions
#
# def print_list(the_list):
#     for i in the_list:
#         if i == "ab" :
#             print("1")
#         elif i == "cd":
#             print("2")
#         elif i == "kl":
#             print("3")
#         else:
#             print("4")
#
# the_list = ['ab', "cd", "ab", "ef", "gh", "ij", "kl", "mn"]
#
#
# print_list(the_list)
#
# #######################################################################################################
#
#
#
#
#
#
# #print(dir(str))
#
# # escape sequence "\"
# print ("shashank is a \
#        rockstar")
# print ('What\'s' ' your name?')
#
# # unicode
# print(u"Shashank is amazing")
#

list1=[1,2,3,4,5,6,7,8,9]
list2=[3,4]

sum1=0
sum2=0

for i in list1:
    for j in list2:
        if j%3==0:
            sum1=sum1+i
        if i%4==0:
            sum2=sum2+i
print(sum1, sum2)

