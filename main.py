import json
import logging
import os
import unittest
import urllib3
import pathlib
import pickle
import re
import subprocess
import keyboard
from selenium.webdriver.chrome.options import Options
# import undetected_chromedriver as webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from pages.home.home_page import HomePage



class TelemetryTest(unittest.TestCase):
    def setUp(self):

        # driver_service = ChromeDriverManager().install()

        # Update download_dir and config_dir paths to be platform-independent
        # config_dir = os.path.abspath(os.path.join(os.getcwd(), "config.json"))
        

        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--start-maximized")
  

        self.driver = webdriver.Chrome(options=chrome_options)

        # Disable SSL warnings and set up logging
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s : %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.getLogger().setLevel(logging.INFO)

        # Load configuration data and test site data from JSON files
        # with open(config_dir, "r") as json_file:
        #     self.config_data = json.load(json_file)
        # with open(testsites_dir, "r") as test_sites_json_file:
        #     self.test_sites_data = json.load(test_sites_json_file)

 
        self.home_page = HomePage(self.driver)


    def test_search_button(self):
        self.home_page.logger("Testing modal appearance on search click...")
        self.home_page.open_search()
        self.home_page.verify_search_modal_elements()
        self.home_page.check_search_by_tire_size_tab()
        self.home_page.check_select_year_dropdown(29)
        self.home_page.click_then_check_wheels_tab()
        self.home_page.check_select_year_dropdown(27)
        self.home_page.click_then_check_packages_tab()
        self.home_page.check_select_year_dropdown(9)

    def test_empty_search(self):
        self.home_page.logger("Testing empty searches...")
        self.home_page.open_search()
        self.home_page.click_then_check_tires_tab()
        self.home_page.check_empty_search()
        self.home_page.click_then_check_wheels_tab()
        self.home_page.check_empty_search()
        self.home_page.click_then_check_packages_tab()
        self.home_page.check_empty_search()

    def test_close_search(self):
        self.home_page.logger("Testing modal close button...")
        self.home_page.open_search()
        self.click_then_check_close_button()
    
    def test_random_search_by_vehicle(self):
        self.home_page.logger("Testing Random Search...")
        self.home_page.open_search()
        self.home_page.random_search_by_vehicle()

    def tearDown(self):
        # Close the browser
        self.driver.quit()
        del self.driver

if __name__ == "__main__":
    # Run the test case
    unittest.main()
