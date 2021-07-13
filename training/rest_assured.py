'''
REpresentational State Transfer [REST]

Rest APIs dont create objects everytime, it sends the state for the existing objects
To make make valid REST requests

Features of REST
1. simpler than SOAP
2. Well Documented
3. Propper logging of the error message

Methods od REST API
CRUD
Create  --> Post
Read    --> Get
Update  --> Put
Delete  --> Delete


'''




'''
RestAssured.given().
    when().
        header(). # auth, accpet type(json/xml)
        param().
        body().
    get().
    then().
        assertThat().
        statuscode();

'''


