import pytest

@pytest.fixture(scope='class')
def setup():
    print("this is where everything starts")
    yield
    print(" this is where everything ends")

@pytest.fixture()
def dataload():
    return ('Shashank', 'Mahadev', 'shank@gmail.com')
