# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from base import BaseTest
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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
        driver.find_element_by_id('acceptButton').click()
        driver.find_element_by_id('submit').click()
        alert = driver.switch_to_alert()
        alert.accept()
        WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.ID,'message')))
        msg = driver.find_element_by_id('message')
        self.assertEqual(msg.is_displayed(), True)
        assert 'zatwierdzono wniosek' in driver.page_source

if __name__ == "__main__":
    unittest.main()