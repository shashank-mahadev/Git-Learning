'''
1. Prime Number/ odd numbers
2. Fibonacci Series
3. sorting numbers
4. Read a file and find anagram
5. Palindrome
6. Count duplicates in list
7. Lambda
8. Map, reduce
9. filter
10. multithreading
11. args, kwargs
12. List comprehension
13. Factorial Numbers
14. reverse string, alternate
15. reverse string without even using indexing
16. Most frequent element in list
17. swap a value without using temp variable
18. sort a list of integer with odd and then even without any temp variable
19. Generators
20. Decorators
21. parenthesis balance
22. method overloading, overriding
23. serialization - deserialization
24. Pytest
25. marashelling
26. hash map



'''

# 1
# numbers only wholy divided by 1 and itself
import functools


def prime(n):
    for i in range(n):
        for j in range(2,i):
            if i%j==0:
                break
        else:
            print(i)

# prime(20)


# 2
# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233....
def fibo(n):
    a=0
    b=1
    c=a+b
    for i in range(n):
        a=b
        b=c
        c=a+b
        print(a)

#fibo(20)

# 3
# Sorting numbers
x=[4,5,1,6,2,1,3,98,0,7,7,0,688]

def quick_sort(seq):

    if len(seq) <= 1:
        return seq
    else:
        pivot = seq.pop()

    lower=[]
    higher=[]

    for i in seq:
        if i > pivot:
            higher.append(i)
        else:
            lower.append(i)
    new_list = quick_sort(lower) + [pivot] + quick_sort(higher)
    return new_list

#print(quick_sort(x))

# 4
# read files and find anagram
strs = ['shs', 'ssh', 'asdsa', 'asdas', 'dcd', 'saked']
def anagram(strs):
    count=[]
    for i in strs:
        for j in strs:
            if i!=j and sorted(i)==sorted(j):
                count.append(i)
    print(count)

# page=open('/Users/unraveldata/PycharmProjects/Shashank/Shiva/shashank/text.txt', 'r')
# for line in page:
#     line=line.strip()
#     line=line.lower()
#     words=list(page)
#     # words=line.split("\n")
#     print(words)

# anagram(strs)

# 5
# Palindrome
str1 = 'shsa'
str2 = 1215121
def palindrome(s):
    string = str(s)
    if string == string[::-1]:
        print('palindrome')
    else:
        print('not palindrome')

#palindrome(str2)

# 6
# count duplicates in list
list1=[1,2,3,4,5,6,7,8,9,9,8,7]
def dup(n):
    count1=[]
    count2=[]
    for i in n:
        if i not in count1:
            count1.append(i)
        else:
            count2.append(i)
    print(count2)
# dup(list1)

# 7
# Lambda
# lambda argument : expression
x = lambda x,y : x+y
# print(x(10,20))

list_orig = [{'make':'ford', 'year':2023},{'make':'landrover', 'year':2027}, {'make':'bugati', 'year':2035}, {'make':'ford', 'year':2013} ]
list_sort = sorted(list_orig, key=lambda x:x['year'])
# print(list_sort)

# 8
# Map reduce
lambda_cube = lambda y: y*y*y
# print(lambda_cube(5))

li = [5, 7, 22, 97, 54, 62, 77, 23, 73, 61]

final_list = list(filter(lambda x: (x%2 != 0) , li))
# print(final_list)

final_list = list(map(lambda x: x*2, li))
# print(final_list)

from functools import reduce
def add(a,b):
    return a+b
x=reduce(add, li)
print(x)
# print ("The maximum element of the list is : ",end="")
# print (functools.reduce(lambda a,b : a if a > b else b,lis))


# 9
# filters
# takes sequence as input and returns sequence based on the function
# Example : filter(function, sequence)

nums=[1,2,3,5,4,6,7,8,9,0]

def ifeven(n):
    return n%2==0

even = list(filter(ifeven,nums))
print(even)
evens = list(filter(lambda n: n%2==0, nums))
print((evens))

# 10
# multithreading
from threading import *
class Hello(Thread):
    def run(self):
        for i in range(50):
            print('hello')

class Hi(Thread):
    def run(self):
        for i in range(50):
            print('Hi')

t1=Hello()
t2=Hi()

# t1.start()
# t2.start()

#12
# List comprehension



# 13
# Factorial numbers
def factorial(n):
    f=1
    for i in range(1, n+1):
        f=f*i
    print(f)
# factorial(0)


# 14
# reverse string alternate

sentance='Shashank was driving home when it rained'

def rev_alt(s):
    word_list=s.split(" ")
    final_list=[]
    for i in range(0, len(word_list)):
        if i%2==0:
            final_list.append(word_list[i][::-1])
        else:
            final_list.append(word_list[i])
    print(final_list)
    final_sent=" ".join(final_list)
    print(final_sent)

# if __name__=="__main__":
#     sentance='Shashank was driving home when it rained'
#     rev_alt(sentance)


#15
# reverese string without even using indexing

def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str

# print(reverse(sentance))



#16
# Most frequent element in list
freq1=[1,2,3,3,4,4,4,4,5,6,6,7,8]
freq2=['sin', 'r', 'sin', 'i', 'ind', 'uiy', 'ind']
def frequent(seq):
    count=0
    temp=0
    index=0
    for x in range(0, len(seq)):
        temp = seq.count(seq[x])

        if (temp>count):
            count=temp
            index=x

    most_freq=seq[index]
    print('frequent element', most_freq, 'and it appeared', count)

# frequent(freq2)


def fib(limit):

    # Initialize first two Fibonacci Numbers
    a, b = 0, 1

    # One by one yield next Fibonacci Number
    while a < limit:
        yield a
        a, b = b, a + b

# Create a generator object
x = fib(5)

# Iterating over the generator object using next
# print(x.next()) # In Python 3, __next__()
# print(x.next())


# Iterating over the generator object using for
# in loop.
# print("\nUsing for in loop")
# for i in fib(5):
#     print(i)



#18
# sort a list of integer with odd and then even without any temp variable

def section_sorting(arr):

    for i in range(len(arr)):
        minimum = i

        for j in range(i + 1, len(arr)):
            if arr[j] % 2 == 0:
                minimum = j

        arr[minimum], arr[i] = arr[i], arr[minimum]

    return arr


# if _name_ == "_main_":
#     arr = [10, 1, 1, 9, 3, 6, 4, 5, 5, 8, 2]
#     print("Before sorting: {}".format(arr))
#     sorted_arr = section_sorting(arr)
#     print("After sorting: {}".format(sorted_arr))



# 20
# Decorators
# passing a function to another function as an argument in order to modify the operation without changing other code
def div(a,b):
    print( a/b )

def smartdiv(func):

    if a>b:
        a,b=b,a
        return func(a,b)

smartdiv()





#21
# parenthesis balance

open_list = ["[","{","("]
close_list = ["]","}",")"]

# Function to check parentheses
def check(myStr):
    stack = []
    for i in myStr:
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and (open_list[pos] == stack[len(stack)-1])):
                stack.pop()
            else:
                return "Unbalanced"
    if len(stack) == 0:
        return "Balanced"
    else:
        return "Unbalanced"
#
# if __name__=='__main__':
#     string = "{]{()}}"
#     print(check(string))
