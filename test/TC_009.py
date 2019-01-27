# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from base import BaseTest
from selenium.webdriver.support import expected_conditions

class Test(BaseTest):

    def test_script(self):
        driver = self.driver
        driver.get('localhost:5000/login')
        uname = driver.find_element_by_id('username')
        pwd = driver.find_element_by_id('password')
        uname.send_keys('admin@wp.pl')
        pwd.send_keys('pokpok')
        driver.find_element_by_id('submit').click()
        driver.get('localhost:5000/forms')
        driver.find_element_by_css_selector("input[type='radio'][value='accept']").click()
        driver.find_element_by_id('submit').click()
        assert 'zaakceptowano wniosek' in driver.page_source