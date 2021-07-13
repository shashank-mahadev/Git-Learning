'''Regular Expressions : are maily used to search some patterns
in regex there are MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

these are special characters in regex. so if u literally have to find/search them, escape the character
ex:
pattern = re.compile(r'.')  ------> instead of searching for the period this searches every character in the file, hence escape using excape character
pattern = re.compile(r'\.') ------> now this only search for period in the file


characters and its functions in regex:
.       - any characters expect new line
\d      - Digit( 0-9 )
\D      - Not a digit ( 0 - 9 )
\w      - word character ( a-z, A-Z, 0-9, _)
\W      - Not a word character
\s      - whitespace ( space, tab, new line )
\S      - Not whitespace
\b      - word boundry
\B      - not a word boundry
^       - begining of the string

anchors: they dont mach any characters they store

\b      - word boundry
\B      - not a word boundry
^       - Begining of the string
$       - End of the string

[]      - which matches from the items in the bracket
[^]     - which matches characters NOT in the bracket
|       - Either or
()      - group

Quantifiers:

*       - 0 or more
+       - 1 or more
?       - 0 or none
{3}     - Exact number
{3-4}   - range of numbers



'''

# raw string = this consider any characters that does a function as text
# example below "\t" stands for new line, but raw string converts it to text
print("\tTab")
print(r"\tTab")


import re
print(dir(re))


test_to_search = '''
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890

Ha Haa

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

shashank.com

888-481-8182
123.481.7890
123*481*7890


Mr. Shashank
Mr Mahadev
Ms Sindhu
Mrs. ramesh
Mr. T
'''

sentance = 'Start sentance and then bring it to an end'


# create a pattern
pattern = re.compile(r'abc')
pattern = re.compile('.') # matches everything except new lines
pattern = re.compile(r'abc')
pattern = re.compile(r'\d')
pattern = re.compile(r'\D')
pattern = re.compile(r'\w')
pattern = re.compile(r'\s')
pattern = re.compile(r'\S')

# create a search using the pattern

match = pattern.finditer(test_to_search)

# print out all the matches

for i in match:
    print (i)


pattern = re.compile(r'end$') # see that this matches end only if the word is at the end of the statement
pattern = re.compile(r'Start$') # see that this matches dont give results as the word "start" is not at the end
pattern = re.compile(r'^end') # see that this matches  only if the word is at the start of the statement
pattern = re.compile(r'^Start') # see that this matches because the word "start" is at start of the statement


match = pattern.finditer(sentance)

for i in match:
    print (i)


'''
now lets try to find the a pattern search for example a phone number given in above "test_to_search". so pattern must be
**3 digit and a dash again 3 digit and a dash and 4 digits**

'''

pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d') # we are using "." as it will match anything
pattern = re.compile(r'\d\d\d[.-]\d\d\d[-.]\d\d\d\d') # by using "[]" this will shown either - or . | this will search for items in the []
pattern = re.compile(r'[1-9]') # to search in a range of characters
pattern = re.compile(r'[a-zA-Z]') # to search in a range of characters


match = pattern.finditer(test_to_search)

for i in match:
    print(i)



