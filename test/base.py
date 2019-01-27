import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_script(self):
        pass

    def tearDown(self):
        self.driver.get("localhost:5000/reset")
        WebDriverWait(self.driver,3)
        self.driver.close()