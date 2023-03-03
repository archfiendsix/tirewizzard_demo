import logging
import urllib3
import pickle
import random
import time
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver,
        
       
    def setup(self):
        pass

    def maximize_window(self):
        self.driver.maximize_window()


    def logger(self, text):
        logging.info(text)

    def wait_and_execute(self, driver, locator, timeout, action):

        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator))
        action(element)
        time.sleep(random.randint(1, 2))
