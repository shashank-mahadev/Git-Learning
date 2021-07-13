import pytest

a=10
b=20

def test_demo():
    print('first statement')

@pytest.mark.smoke
def test_add(num1,num2):
    return num1+num2
assert test_add(20,10) == 30, "addition dint match"



if __name__=="__main__":
    a=10
    b=20