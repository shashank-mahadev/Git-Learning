# for and while
# break and continue statements
import os
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for things in nums:
    print(things)

########

for things in nums:
    if things == 7:
        print ("this is it, found " )
        break
    print(things)

#########

names = ['shashank', 'chetan', 'chandan', 'ashwattama', 'drona', 'karna', 'krishna', 'arjuna', 'drona']

for persons in names:
    if persons == "krishna":
        print("architect of mahabaratha is krishna")
        break
    print(persons)

##############

for i in range(10):
    for letters in "shashank":
        print(i, letters)


# while loops

print("Starting while loop")

x = 0
# while x < 10:
#     print (x)
#     x += 1

while x < 10:
    if x == 5:
        break
    print (x)
    x +=1



####################################

print("another while loop")

i=1

while i <= 10:
    print(i+1)
    break


print("another while loop")



# i = int(input("enter integer"))
# j = int(input("enter integer"))
# while i < 10:
#     while j == 5:
#         print(i, j)
#         i=i+1
#         j=j-1


print("another while loop")
