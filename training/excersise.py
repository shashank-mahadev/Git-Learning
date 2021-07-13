# # # max of the numbers
# #
# # list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
# #
# # def find_max(list):
# #     max = list1[0]
# #     for i in list1:
# #         if i > max:
# #             max = i
# #     return max
# #
# # print(find_max(list1))
# #
# # def find_largest(list):
# #     list.sort()
# #     print(list)
# #     largest_num = list[-1]
# #     print(largest_num)
# # print(find_largest(list1))
# #
# # # max of 2 numbers
# #
# # def max_of_two(a, b):
# #     if a > b:
# #         print(a)
# #     else:
# #         print(b)
# #
# #
# # max_of_two(3, 9)
# #
# #
# # # factorial
# # # Example: 4! = 4*3*2*1
# #
# # def facto(n):
# #     return 1 if (n==1 or n==0) else n * facto(n-1)
# #
# # print(facto(6))
# #
# # # simple interest
# # '''
# # Simple Interest = (P x T x R)/100
# # Where,
# # P is the principle amount
# # T is the time and
# # R is the rate
# # '''
# #
# # def simple_interest(p,t,r):
# #     r = r/100
# #     si = r*t*p
# #     print(si)
# #
# # simple_interest(100000, 1, 5)
#
# # prime numbers
# '''
# prime numbers are natural number which are divisible by exactly 2 numbers,  itself and '1'.
# '''
#
#
# # def prime(num):
# #     flag = False
# #     if num > 1:
# #         for i in range(2, num):
# #             if (num % i) == 0:
# #                 flag = True
# #                 break
# # if flag:
# #     print( num, " it is not prime number")
# # else:
# #     print (num, "is a prime number")
# # prime(2)
#
# # import sympy
# # print (sympy.isprime(5))
#
# # # palindrome
# # def palindrome(s):
# #     i = str(s)
# #     j = i[::-1]
# #     if i == j:
# #         print(i, 'is palindrome')
# #     else:
# #         print(i, 'is not a palindrome')
# #
# # palindrome('brasarb')
#
# sent = "Shashank is on wheels"
# # def reverse_sent(sent):
# # sent = "Shashank is on wheels"
# # i = sent.split(' ')
# # j = i[::-1]
# # k = ' '.join(j)
# #     print(' '.join((sent.split(' '))[::-1]))
#
# # reverse_sent_words("how many assholes in world")
#
# # def reverse_letter_in_sent(sent=input()):
# #     rev_sent = sent.split(' ')
# #     final_list=[]
# #     for i in rev_sent:
# #         final_list.append(i[::-1])
# #         final_sent = ' '.join(final_list)
# #     print(final_sent)
# #
# # reverse_letter_in_sent()
#
# ## Replace a character in the string
#
# # def remove_char(sent):
# #     new = sent.replace('a', '', 1)
# #     print(new)
# #     new_str = sent[:2] +  sent[3:]
# #     print(new_str)
# #
# # remove_char(sent)
#
# ## Check if a Substring is Present in a Given String
#
# # def check_substring(string, substring):
#
# # string = 'Shashank is in Black Pearl, the iconic ship'
# # substring = 't'
# # def check_substring(string, substring):
# #     if (string.find(substring)) == -1:
# #         print("not")
# #     else:
# #         print('present')
# #
# # check_substring(string, substring)
# #
# #
# # def reverse(string):
# #     reverse_str=string[::-1]
# #     print(reverse_str)
# # reverse('shank')
# #
#
# '''
#
# If  is odd, print Weird
# If  is even and in the inclusive range of 2 to 5, print Not Weird
# If  is even and in the inclusive range of 6 to 20, print Weird
# If  is even and greater than 20, print Not Weird
# '''
#
#
#
# #
# # if n in range(1, 101):
# #     if n%2 == 0:
# #         if n in range(2, 6):
# #             print(' Not weird ')
# #         elif n in range(6, 21):
# #             print('Weird')
# #         elif n > 20:
# #             print('Not Weird')
# #     else:
# #         print('Weird')
# # else:
# #     print('number should be lesser than 100 ')
#
#
# # if __name__ == '__main__':
# #     a = int(input())
# #     b = int(input())
# #
# # print (f'{a+b}\n{a-b}\n{a*b}')
#
#
# #
# #
# # def avg(arg1, *args):
# #     list1=[]
# #     for i in args:
# #         list1.append(i)
# #     list1.append(arg1)
# #     x=len(list1)
# #     y=sum(list1)
# #     z=y/x
# #     return z
# #
# #
# # avg(2, 3, 4, 6, 566, 78)
# #
# # class Car():
# #     def __init__(self, max_speed, speed_unit):
# #         self.max_speed = max_speed
# #         self.speed_unit = speed_unit
# #         print(f'Car with the maximum speed of {self.max_speed} {self.speed_unit}')
# #
# # class Boat:
# #     def __init__(self, max_speed):
# #         self.max_speed=max_speed
# #         print(f'Boat with the maximum speed of {self.max_speed} knots')
# #
# # car = Car(120, 'kmh')
# # boat = Boat(12)
#
#
# # n = 5
# # list1=[]
# # for i in range(1, n):
# #     print(i, end='')
#
# # # fibonacii
# # # Ex: 0,1,1,2,3,5,8,13,21,34...
# #
def fibo(n):
    a=0
    b=1
    list1=[0]
    for i in range(n):
        z=a+b
        a=b
        b=z
        list1.append(a)
    print(list1)
fibo(10)
# #
# #
# # #Factorial
# #
# # def factorial(n):
# #     f=1
# #     for i in range(1, n+1):
# #         f=f*i
# #     return f
# # print(factorial(5))
#
# def prime(n):
#     for i in range(2, n):
#         if n%i==0:
#             print('not prime')
#             break
#     else:
#         print('prime')
#
# prime(1)
#
# import random
# import string
# # l=[]
# # for i in range(20):
# #     l.append(round(random.random(),2))
# # print(l)
# #
# # print(random.choice(['heads', 'tails']))
# #
# # l2=[]
# # for i in range(20):
# #     l2.append(random.choice(string.ascii_uppercase)+random.choice(string.ascii_uppercase))
# # print(l2)
# #
# # print(random.sample(string.ascii_uppercase,26))
#
# ##########
#
# # import random
# # ls = []
# # for i in range(10):
# #     x=random.randint(1,100)
# #     ls.append(x)
# # print(ls)
# #
# # x= [random.randint(1,100) for i in range(10)]
# # print(ls)
#
#
# import string
# import random
# # ls1=[]
# # print(string.ascii_uppercase)
# # for i in string.ascii_uppercase:
# #     ls1.append(i)
# # print(ls1)
# #
# # ls2=[string.ascii_uppercase for i in range(10)]
# # print(ls2)
# #
# # s1=[1,2,3,4,5]
# # s2=[9,8,7,6,5]
# # print(list(zip(s1,s2)))
# #
#
# #
# # ls_names=['Emma','Silvia','Bryan','Hannah','John','Kim','Martha','Kevin','Bob','Mary','Ben','Alex','Tim','Don','Ken','Roger','Joan','Stan','Peggy','Bert','Rick','Oliver','Noah','Oscar','Evelyn','Florence','Theo','Isabella','Lily','Ava']
# # names=random.sample(ls_names,10)
# # sscores=[[random.randint(40,100) for i in range(5)] for j in range(10)]
# # print(dict(zip(names,sscores)))
# #
# # c=dict(zip(random.sample(ls_names,10),[[random.randint(40,100) for i in range(5)] for j in range(10)]))
# # print(c)
# #
# # for i in c.items():
# #     i[2]=i+10
# # print(c.items)
#
# # def factor(s):
# #     f=1
# #     for i in range(1, s+1):
# #         f = f*i
# #     return f
# #
# # print(factor(5))
# #
# # def prime(n):
# #     for i in range(2, n):
# #         if n%i==0:
# #             print('not prime')
# #             break
# #     else:
# #         print('prime')
# #
# # prime(7)
# #
# arr=[1,2,8,4,5,6,7,7,8,1]
# s = 'shashank was, here everytime'
# # s=['shank', 'shamak', 'shashank', 'shank']
#
# # s1 = "learning python is not so difficult as we think"
# #
# # def rev_str(s1):
# #     elements = s1.split(" ")
# #     reversed_elements = list()
# #     for i in range(0, len(elements)):
# #         if i % 2 == 0:
# #             reversed_elements.append(elements[i][::-1])
# #         else:
# #             reversed_elements.append(elements[i])
# #
# #     print(" ".join(reversed_elements))
# # rev_str(s1)
# #
# # # Write a program to read a file and find Anagram words.
# # f = open("text.txt", "r")
# # f = f.readlines()
# #
# # anagram_list = []
# # for word_1 in f:
# #     for word_2 in f:
# #         if word_1 != word_2 and sorted(word_1)==sorted(word_2):
# #             anagram_list.append(word_1.strip('\n'))
# # print(set(anagram_list))
#
#
# def instertion_sort(arr):
#     for i in range(1, len(arr)):
#         j=i
#         while arr[j-1] > arr[j]:
#             arr[j-1], arr[j] = arr[j], arr[j-1]
#             # j-=1
#             j=j-1
#
# instertion_sort(arr)
# print(arr)
#
#
# def reverse_string(s):
#     rev = s[::-1]
#     return rev
#
#
# def reverse_alternate_value(s):
#     s1 = s.split(" ")
#     complete_string = list()
#     for i in range(len(s1)):
#         if i % 2 == 0:
#             complete_string.append(s1[i])
#         else:
#             complete_string.append(s1[i][::-1])
#
#     return complete_string
#
# print(reverse_alternate_value(s))
#
#
# for i in range(20):
#     print(i%2)
#
#
# N = [6,7,1,2,3,4,5,6,7,8,9]
# N.remove(7)
# print(N)


def rev_sent(s):
    s1=s.split(" ")
    z=[]
    for i in s1:
        if i % 2 == 0:
            z.append(s1(i))
        else:
            z.append(s1(i)[::-1])



#
# def list_mod(repl):
#     N[i]=e
#     print(N)
#     N.remove(repl)
#     list.append(N)
#     list.sort
#     list.pop
#     list[::-1]

# # list_mod(5)
# def leapyear(n):
#     if n%4==0:
#         print(n, "is leap year")
#     elif n%400==0 and n%100!=0:
#         print(n, 'is a leap year')
#     else:
#         print(n, 'is not a leap year')
#
#
# leapyear(2100)

import math
import os
import random
import re
import sys

# Complete the sockMerchant function below.
# n=9
ar=[-1, 10, 20, 20, 10, 10, 30, 50, -2, 10, 20]
br=['shank','shan','shashank','shank','shash']
#
# def sockMerchant(a):
#     match=[]
#     for i in range(len(a)):
#         for j in range(i+1, len(a)):
#             if a[j]==a[j]:
#                 match.append(a[i])
#     print(match)
#
# sockMerchant(ar)
#

# def sockMerchant(a):
#     # print("a is {}".format(a))
#     match=[]
#     for i in a:
#         # print("aaa {}".format(i))
#         for j in a:
#             if i == j:
#                 match.append(i)
#     print(match)

#
#
#
#
# def quicksort(x):
#     if len(x)<=1:
#         return x
#     else:
#         pivot=x.pop()
#     left=[]
#     right=[]
#     for i in x:
#         if i>pivot:
#             right.append(i)
#         else:
#             left.append(i)
#     new_list = quick_sort(left)+[pivot]+quick_sort(right)
#     print(new_list)
#     print(new_list[-1])
#
# print(quicksort(ar))
#
#
#
#
#
# anagram1 = ['shashank', 'nkshasha', 'slice', 'sliec', 'rainbow', 'bollo']
#
# def anagram(x):
#     anag=[]
#     for i in x:
#         for j in x:
#             if i!=j and sorted(i)==sorted(j):
#                 anag.append(i)
#     print(sorted(anag))
#
# anagram(anagram1)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# def shank_sort(array):
#     if len(array)<=1:
#         return array
#     else:
#         pivot = array.pop()
#
#     low_side=[]
#     high_side=[]
#
#     for i in array:
#         if i > pivot:
#             high_side.append(i)
#         else:
#             low_side.append(i)
#     return shank_sort(low_side)+[pivot]+shank_sort(high_side)
#
# shank_sort(ar)
#
#
#
#
#
#
#
#
#
#
# seq=[1,2,3,1,2,3,9,8,7,8,6,7,65,0,9,-1,-3,7888]
# def sort(sequence):
#     if len(sequence) <= 1:
#         return sequence
#     else:
#         pivot = sequence.pop()
#
#     lower_count=[]
#     higher_count=[]
#
#     for i in sequence:
#         if i>pivot:
#             higher_count.append(i)
#         else:
#             lower_count.append(i)
#     return sort(lower_count)+[pivot]+sort(higher_count)
#
# new_list=sort(seq)

seq=[8,7,5,4,2,1,8,9,5,6]

def sort_quick(seq):

    if len(seq) <=1:
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

    sorted_seq=sort_quick(lower)+[pivot]+sort_quick(higher)
    return sorted_seq

print(sort_quick(seq))




#
# print(f'the sorted sequence is {new_list}')
# print(f'the sorted sequence is {new_list[0]}')
#
# print(f'the max in the list is {new_list[-1]}')
# # print(f'the max in the list is {(sort(seq)[0])}')
# #
#
#
# def anag(ana):
#     ana_list=[]
#     for i in ana:
#         for j in ana:
#             if i!=j and sorted(i)==sorted(j):
#                 ana_list.append(i)
#     print(ana_list)
#
# anag(anagram1)
#
# def facto(n):
#     num=[]
#     for i in range(1, n+1):
#         num.append(i)
#     result=1
#     for j in num:
#         result=result*j
#     return result
#
# print(facto(10))
#
#
#
# def fac(n):
#     result=1
#     for i in range(1, n+1):
#         result=result*i
#     return result


#
#
# pali = ['sahas', 'ghg', 'shank', 'deer']
# pali1 = [121, 323, 44544, 123]
#
# print(str(pali1))
# x=str(pali1)
# print(x)

#
# def palindrome(y):
#     x=str(y)
#     print(x)
#     shank=[]
#     for i in x:
#         if i==i[::-1]:
#             shank.append(i)
#     return [shank]
#
#
# print(palindrome(pali1))

s1 = "learning python is not, so difficult as we think"

#
# def rev_str(s1):
#     elements = s1.replace(",", " ")
#     print(elements)
#     elements = elements.split(" ")
#     print(elements)
#     reversed_elements = list()
#     for i in range(0, len(elements)):
#         if i % 2 == 0:
#             reversed_elements.append(elements[i][::-1])
#         else:
#             reversed_elements.append(elements[i])
#
#     print(" ".join(reversed_elements))
#
# rev_str(s1)





#
# def reverse(string):
#     elements=string.replace(",", " ")
#     elements=elements.split(" ")
#     reversed_string=[]
#     for i in range(0, len(elements)):
#         if i % 2 == 0:
#             reversed_string.append(elements[i])
#         else:
#             reversed_string.append(elements[i][::-1])
#     print(reversed_string)
#     print(" ".join(reversed_string))
#
# reverse(s1)



#
# def reverse(x):
#     str_list=x.replace(",", "")
#     str_list=str_list.split(" ")
#     reverse_list=[]
#     for i in range(0, len(str_list)):
#         if i%2==0:
#             reverse_list.append(str_list[i])
#         else:
#             reverse_list.append(str_list[i][::-1])
#     return " ".join(reverse_list)
#
# print(reverse(s1))
#





#
# def oolta(padagalu):
#     padagala_patti=padagalu.split(" ")
#     oolta_patti=[]
#     for i in range(0,len(padagala_patti)):
#         if i%2==0:
#             oolta_patti.append(padagala_patti[i])
#         else:
#             oolta_patti.append(padagala_patti[i][::-1])
#     print(oolta_patti)
#     print(' '.join(oolta_patti))
#     return ' '.join(oolta_patti)
#
# oolta(s1)
#
#
#
# num = int(input('Pls enter the number'))
# c = 2
# while num != 0:
#     for i in range(2, c):
#         if c % i == 0:
#             break
#         else:
#             print(c, end=" ")
#             num -= 1
#         c += 1




class Calculator:
    num = 100
    def __init__(self, a, b):
        self.a=a
        self.b=b

    def add(self):
        return self.a+self.b
    def sub(self):
        return self.a-self.b
    def over(self):
        return self.a+self.b+Calculator.num

class Div(Calculator):
    num2=200
    def divi(self):
        return self.a/self.b
    def misc(self):
        return Calculator.num+Div.num2+self.add()


x=Calculator(2,3)
print(x.add())
print(x.over())

y=Div(6,5)
print(y.add())
print(y.divi())
print(y.misc())

































