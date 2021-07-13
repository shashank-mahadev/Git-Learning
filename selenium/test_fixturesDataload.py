import pytest
from selenium.BaseClass import BaseClass


@pytest.mark.usefixtures("setup")
class TestExample:

    def test_second(self):
        print('second statement')

    # @pytest.mark.smoke
    # @pytest.mark.skip
    def test_reverse(self):
        print('second test man')

    # @pytest.mark.xfail
    def test_check1(self):
        print("just testing1")

@pytest.mark.usefixtures("dataload")
class TestingFixtures(BaseClass):

    def test_name(self, dataload):
        log = self.getLogger()
        log.info(dataload[0])
        print(dataload[0])
    def test_lastname(self, dataload):
        print(dataload[1])
    def test_email(self, dataload):
        print(dataload[2])

