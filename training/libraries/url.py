import urllib.request
import time
import requests

def webconnect1(url1):
    # url1 = "http://google.com/"
    final_exception = None
    for i in range(5):
        time.sleep(2)
        try:
            web_page = urllib.request.urlopen(url1)
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


def webconnect2(url):

    Error_shown = None
    for i in range(5):
        try:
            web_page = requests.get(url)
            time.sleep(2)
            if web_page.status_code == 200:
                print("Web page opened successfully with code :", web_page.status_code)
                break
        except Exception as e:
            Error_shown = e
            print("The Error is", Error_shown)

    if Error_shown is not None:
        raise Error_shown