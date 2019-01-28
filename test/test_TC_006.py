# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from base import BaseTest
from selenium.webdriver.support import expected_conditions

class Test(BaseTest):

    def test_script(self):
        driver = self.driver
        driver.get('localhost:5000/forms')
        assert u'brak uprawnień' in driver.page_source


if __name__ == "__main__":
    unittest.main()