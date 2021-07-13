'''

API Test Website ---> https://reqres.in/

API - Application Programming Interface

REST API:
it focuses on system resources and how state of resource should be transported over HTTP protocol to different clients
written in different language

Uses RESTFUL Web Services, each URI/Global ID is a resource in REST API




Architucture:
Use HTTP for client-server communication
XML/JSON as formatting language
Simple URI as the address for the services
Stateless  communication

Major constraints :
Uniform Interface
Stateless
Cacheable
Client-Server
Layered system
code on demand


Methods:
GET, PUT, POST, PATCH
GET: It requests a resource at the request URL. It should not contain a request body as it will be discarded. Maybe it can be cached locally or on the server.
POST: It submits information to the service for processing; it should typically return the modified or new resource, duplication is possible
PUT: At the request URL it update the resource
DELETE: At the request URL it removes the resource
OPTIONS: It indicates which techniques are supported
HEAD: About the request URL it returns meta information, Its GET request without response body
PATCH: Always update the data, if the identifier doesnt exist then it will throw the exception



Testing:
1. Validated APIs with min and max
2. Schema Validation, XML and Json
3. Verify the Respone
4. Error codes are Handled
5. Performance of APIs


HTTP Status code:

1xx: Informational message
2xx: Successful
3xx: Redirection
4xx: Client Error
5xx: Server Error

100- continue
200- Success request
200- Success post/create
202- Accept-execute later
204- no content/no response
400- bad request-- invalid schema/cannot convert datatype
403- forbidden / not authorised
404- Not found
405- Not allowed
406- Not acceptable
500- Internal server error
503- service unavailable(maintainance)









'''


from shashank.notes.spark_submit import run_spark
import requests

app_name = run_spark

def api_req(self, url, app_id)
    self.url = "http://fargo13.unraveldata.com:7180/api/v1/clusters"
    self.app_id = app_name
    path = f"{self.url}/{app_id}"
    auth1 = requests.get(path, auth=("admin", "admin"))
# print(auth1.text)

    response1 = auth1.json()
