import json



'''
Conversion of Jason to Python

Json          Python
====          ======

Object        Dictonary
array         List
String        str
number(int)   int
number(real)  Float
true          True
false         False
null          None

'''


sample = '''
    
{
  "states": [
    {
      "name": "Alabama",
      "abbreviation": "AL",
      "area_codes": ["205", "251", "256", "334", "938"]
    }
  ]
}
'''

data = json.loads(sample)
# print(data)

for i in data['states']:
    print(i['name'])
    print(i['abbreviation'])
    print(i)
    del i['name']
    print(i)






with open('states.json') as f:
    data = json.load(f)
for i in data['states']:
    print(i['name'])

with open('states.jason', 'w') as f:
    json.dump(data, f, indent=2)
    





