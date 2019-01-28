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
		driver.get('localhost:5000/register/admin')
		name = driver.find_element_by_id('name')
		surname = driver.find_element_by_id('surname')
		email = driver.find_element_by_id('username')
		password = driver.find_element_by_id('password')
		name.send_keys('Andrzej')
		surname.send_keys('Testowy')
		email.send_keys('admin@wp.pl')
		password.send_keys('Testtest')
		driver.find_element_by_id('submit').click()
		WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.ID,'message')))
		assert 'uzytkownik z tym emailem juz istnieje' in driver.page_source
		
if __name__ == "__main__":
    unittest.main()