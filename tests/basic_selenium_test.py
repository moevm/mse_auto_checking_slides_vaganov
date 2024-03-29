import os
import unittest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasicSeleniumTest(unittest.TestCase):

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    '''
    If you want to run tests just from Dockerfile_selenium, you can use:

    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(options=chrome_options, service=service)
    instead of 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    '''

    def authorization(self):
        host, login_param, password_param = self.param[:3]
        URL = self.get_url('/login')
        self.get_driver().get(URL)
        self.get_driver().implicitly_wait(30)
        login = self.get_driver().find_element(By.ID, "login_text_field")
        login.clear()
        login.send_keys(login_param)
        password = self.get_driver().find_element(By.ID, "password_text_field")
        password.clear()
        password.send_keys(password_param)
        login_button = self.get_driver().find_element(By.ID, "login_button")
        login_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "upload_upload_button")))


    def __init__(self, methodName='runTest', param=None):
        super(BasicSeleniumTest, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_class, param=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(name, param=param))
        return suite

    def get_url(self, relativePath):
        return self.param[0] + relativePath

    def get_driver(_):
        return BasicSeleniumTest.driver

    @classmethod
    def close_driver(cls):
        cls.driver.close()
