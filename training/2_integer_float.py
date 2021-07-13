num1=12856
num2=789.35
name="shank"
print (type(num1))
print (type(num2))
print (type(name))

'''
Arithmetic operators  
addition             : 3 + 2
substraction         : 
multiplication       : 
division             : 3 / 2 = 1.5
floor division       : 3 // 2 = 1  # truncates decimal values and give whole
exponent             : 3 ** 2 = 9
modulous             : 3 % 2  = 1

'''

print (3 % 2) # mod is usually used to identify odd/even numbers which gives 1/o always when divided by 2

# order of operation
print (3*2+1)
print (3 * (2 + 1))

# increment
num = 10
num += 2 # increment by 2
num *= 5 # multiply by 5

print (num)

num3 = -5

print (abs(num3)) # removes negative  and give absolute value

print (round(num2)) # rounds off to approx values

print (round (3.7767674, 3)) # rounds off approx 3 digits after decimal point


'''
Comparision
equal               == 
not equal           !=
greater than        >
lesser than         <
greater or equal    >=
lesser or equal     <=

above returnes boolean values
'''

print (2>=4)


# casting

num_1="100"
num_2="200"


print ((int(num_1)) + (int(num_2)))



num_1 = int(num_1)
num_2 = int(num_2)

print (num_2 + num_1)



