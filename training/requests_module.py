# HTTP for Humans


import requests
import json_test
import jsonschema

# r = requests.get('https://xkcd.com/353')
# r1 = requests.get('https://imgs.xkcd.com/comics/python.png')
# print(r)
#
# # print(dir(r))
# # print(help(r))
# #print(r1.content)
# print(r.text)
#
# with open('comic.png', 'wb') as z:  # "wb" is write-byte mode
#     z.write(r1.content)
#
# print(r.status_code)
#
# # codes meaning
# # 200 - OK/ Success
# # 300 - redirect
# # 400 - client errors / permission not there
# # 500 - server error / server crash
#
# print (r.headers)
#
# # HTTP method doc
# # https://httpbin.org/#/HTTP_methods
#
# payload = {'page':2, 'count':25 }
#
# h = requests.get('https://httpbin.org/get', params=payload)
# i = requests.post('https://httpbin.org/get', params=payload)
#
# print(h.text)
# print(h.url)
# print(h.json())
#
# h_dict = h.json()
# #print(h_dict)
# print(h_dict['headers'])
# print(h_dict['args'])

# authentication

# auth = requests.get("https://httpbin.org/basic-auth/shashank/password", auth=('shashank', 'password'))
# print(auth.text)
# print(auth)

auth1 = requests.get("http://fargo13.unraveldata.com:7180/api/v1/clusters", auth=("admin", "admin"))
# print(auth1.text)

response1 = auth1.json()
response = json_test.loads(auth1.text)
# print(response)

# print(response1[''][0]["name"])
# print(response1['items'][0]["version"])

for res in response1["items"]:
    host = (res["name"])

url1 = f"http://fargo13.unraveldata.com:7180/api/v1/clusters/{host}/services"
print(url1)
response2 = (requests.get(url1, auth=("admin", "admin")).json())
# print(response2)

for res2 in response2["items"]:
    results = requests.get(res2["serviceUrl"])
    results2 = ((res2["serviceUrl"]) + "xyz")
    if results.status_code == 200:
        print(f"this url is success {res2['serviceUrl']} with status code {results.status_code}")
    else:
        print(f"this url is failed {res2['serviceUrl']} with status code {results.status_code}")
