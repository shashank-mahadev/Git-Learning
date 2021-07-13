'''
open the webpage using a browser
use retry for the response
check the status
check the content
input the search item


'''
import urllib.request
import time
import json
import requests as req


url = "http://google.com/"
final_exception = None
for i in range(5):
    time.sleep(2)
    try:
        web_page = urllib.request.urlopen(url)
        if web_page.getcode() == 200:
            print("WEB PAGE OPENED SUCCESSFULLY WITH CODE : ", web_page.getcode())
            break
    except Exception as e:
        final_exception = e
        print("Exception is :", final_exception)


if final_exception is not None:
    raise final_exception
else:
    print("Working as expected")

web_page = urllib.request.urlopen(url)
data = web_page.read().decode()
print(data)


