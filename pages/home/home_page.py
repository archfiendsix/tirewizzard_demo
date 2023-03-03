import time
import json
import logging
import requests
import random
import time
from selenium import webdriver
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.search_modal_locator = (By.CSS_SELECTOR, ".search-modal")
        self.home_search_button_locator = (By.CSS_SELECTOR, ".iconbutton.stat-button-link")
        self.select_year_dropdown = (By.CSS_SELECTOR, ".vehicle-selection-options-year")
        self.select_make_dropdown = (By.CSS_SELECTOR, ".vehicle-selection-options-make")
        self.select_model_dropdown = (By.CSS_SELECTOR, ".vehicle-selection-options-model")
        self.curtain_locator = (By.CSS_SELECTOR, ".curtain")
        self.tires_tab_button_locator =(By.XPATH, "//li[contains(text(), 'Tires')]")
        self.wheels_tab_button_locator  =(By.XPATH, "//li[contains(text(), 'Wheels')]")
        self.packages_tab_button_locator =(By.XPATH, "//li[contains(text(), 'Packages')]")
        self.select_year_options = (By.CSS_SELECTOR, ".vehicle-selection-options-year .no-print li")
        self.modal_search_button_locator = (By.CSS_SELECTOR, ".vehicle-selection-button-search .btn.stat-button-link")
        self.search_by_vehicle_tab_locator = (By.XPATH, "//span[contains(text(), 'Search by Vehicle')]")
        self.search_by_tire_size_tab_locator = (By.XPATH, "//span[contains(text(), 'Search by Tire Size')]")
        self.tire_size_search_label_locator = (By.XPATH, "//div[contains(text(), 'Tire Size Search:')]")
        self.question_mark_locator = (By.CSS_SELECTOR, ".fa.fa-question-circle.stat-image-link")
        self.how_to_find_your_tire_size_label = (By.XPATH, "//span[contains(text(), 'How to find your tire size (Tire Size Diagram)')]")
        self.tire_size_close_button_locator = (By.CSS_SELECTOR, ".close-icon.stat-button-close")
        self.search_close_button_locator = (By.CSS_SELECTOR, ".search-wrapper .close-x.stat-button-close")
        self.search_result_year_locator = (By.XPATH, "(//container[@class='side small']//span)[1]" )
        self.search_result_make_locator = (By.XPATH, "(//container[@class='side small']//span)[2]" )
        self.search_result_model_locator = (By.XPATH, "(//container[@class='side small']//span)[3]" )

    def open_search(self): 
        self.driver.get("https://app.tirelocator.ca/gmdealer/en")

        
        self.wait_and_execute(self.driver,self.home_search_button_locator , 10, lambda elem: elem.click())
        self.check_curtain_visible()
        self.check_search_modal_visibility()

    def check_search_modal_visibility(self):
        self.logger("Checking Search Modal Visibility...")
        search_modal = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.search_modal_locator)
        )
        assert search_modal.is_displayed(), "Search Modal Not Present"
        self.logger("Search Modal Present")

    def check_curtain_visible(self):

        curtain_visibility =  self.wait_and_execute(self.driver,self.curtain_locator , 30, lambda elem: elem.is_displayed())
        while curtain_visibility:
            self.logger("Curtain loader still on page")
            time.sleep(1)
            curtain_visibility = self.wait_and_execute(
                self.driver, 
                self.curtain_locator, 
                30, 
                lambda elem: elem.is_displayed()
            )
    
    def verify_search_modal_elements(self):
        self.logger("Verifying search modal elements...")
        time.sleep(6)
        # tires_tab_visibility = self.wait_and_execute(self.driver,self.wheels_tab_button_locator , 10, lambda elem: elem.is_displayed())
        # self.logger(tires_tab_visibility)
        tires_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.tires_tab_button_locator)
        )
        assert tires_tab.is_displayed(), "Tires Tab Not Present"
        self.logger("Tires Tab Present")
        wheels_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.wheels_tab_button_locator)
        )
        assert wheels_tab.is_displayed(), "Wheels Tab Not Present"
        self.logger("Wheels Tab Present")
        packages_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.packages_tab_button_locator)
        )
        assert packages_tab.is_displayed(), "Packages Tab Not Present"
        self.logger("Packages Tab Present")

        self.logger("Search Modal elements verified...")

    def check_select_year_dropdown(self, expected_count):
        wait = WebDriverWait(self.driver, 10)
        self.wait_and_execute(self.driver, self.select_year_dropdown, 10, lambda elem : elem.click())
        li_elements = wait.until(EC.presence_of_all_elements_located(self.select_year_options))
        li_count = len(li_elements)
        assert li_count==expected_count

    def check_search_by_tire_size_tab(self):
        self.logger("Checking Search by Tire Size Tab")
        self.wait_and_execute(self.driver, self.search_by_tire_size_tab_locator, 5, lambda elem: elem.click())
        tire_size_search_label = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.tire_size_search_label_locator)
        )
        assert tire_size_search_label.is_displayed(), "Did not go to Tire Size Search tab"
        self.logger("In Tire Size Search tab ")
        self.wait_and_execute(self.driver, self.question_mark_locator, 5, lambda elem: elem.click())
        how_to_find_tire_size_label = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.how_to_find_your_tire_size_label)
        )
        assert how_to_find_tire_size_label.is_displayed(), "Tire Size Manual Modal did not appear"
        self.logger("Tire Size Manual Modal appeared")
        
        

        self.wait_and_execute(self.driver, self.tire_size_close_button_locator, 5, lambda elem: elem.click())
        
        self.logger("Tire Size Manual Modal closed")



        self.wait_and_execute(self.driver, self.search_by_vehicle_tab_locator, 5, lambda elem: elem.click())
        self.logger("Search by Tire Size Tab Checked")

    def click_then_check_tires_tab(self):
        self.logger("Checking tires tab")
        self.wait_and_execute(self.driver, self.tires_tab_button_locator, 5, lambda elem: elem.click())
        self.check_curtain_visible()

    def click_then_check_wheels_tab(self):
        self.logger("Checking wheels tab")
        self.wait_and_execute(self.driver, self.wheels_tab_button_locator, 5, lambda elem: elem.click())
        self.check_curtain_visible()

    def click_then_check_packages_tab(self):
        self.logger("Checking packages tab")
        self.wait_and_execute(self.driver, self.packages_tab_button_locator, 5, lambda elem: elem.click())
        self.check_curtain_visible()

    def check_empty_search(self):
        self.logger("Testing Empty Search")
        self.wait_and_execute(self.driver, self.modal_search_button_locator, 5, lambda elem: elem.click())
        self.check_search_modal_visibility()

    def click_then_check_close_button(self):
        self.logger("Closing search modal")
        self.wait_and_execute(self.driver,self.search_close_button_locator,10, lambda elem: elem.click())

    def random_search_by_vehicle(self):

        
        search_entries = []
        self.wait_and_execute(self.driver, self.select_year_dropdown, 10, lambda elem: elem.click())
        options = self.driver.find_elements(By.CSS_SELECTOR, '.vehicle-selection-options ul.no-print li.combo-box-value.stat-dropdown span')
        random_index = random.randint(0, len(options) - 1)
        random_option = options[random_index]

        # scroll the page to bring the element into view
        self.driver.execute_script("arguments[0].scrollIntoView();", random_option)

        actions = ActionChains(self.driver)
        actions.move_to_element(random_option).click().perform()

        search_entries.append(self.wait_and_execute(self.driver, self.select_year_dropdown, 10, lambda elem: elem.text))

        options = self.driver.find_elements(By.CSS_SELECTOR, '.vehicle-selection-options-make ul.no-print li.combo-box-value.stat-dropdown span')
        random_index = random.randint(0, len(options) - 1)
        random_option = options[random_index]

        # scroll the page to bring the element into view
        self.driver.execute_script("arguments[0].scrollIntoView();", random_option)

        actions = ActionChains(self.driver)
        actions.move_to_element(random_option).click().perform()

        search_entries.append(self.wait_and_execute(self.driver, self.select_make_dropdown, 10, lambda elem: elem.text))

        options = self.driver.find_elements(By.CSS_SELECTOR, '.vehicle-selection-options-model ul.no-print li.combo-box-value.stat-dropdown span')
        random_index = random.randint(0, len(options) - 1)
        random_option = options[random_index]

        # scroll the page to bring the element into view
        self.driver.execute_script("arguments[0].scrollIntoView();", random_option)

        actions = ActionChains(self.driver)
        actions.move_to_element(random_option).click().perform()

        search_entries.append(self.wait_and_execute(self.driver, self.select_model_dropdown, 10, lambda elem: elem.text))

        # self.logger(f'Searching {search_entries}...')

        self.wait_and_execute(self.driver, self.modal_search_button_locator, 10, lambda elem: elem.click())
        
        self.logger("Checking Search Result Year...")
        search_result_year = self.wait_and_execute(self.driver, self.search_result_year_locator, 10, lambda elem: elem.text)
        assert search_result_year==search_entries[0]
        self.logger("Checking Search Result Make...")
        search_result_make = self.wait_and_execute(self.driver, self.search_result_make_locator, 10, lambda elem: elem.text)
        assert search_result_year==search_entries[1]
        self.logger("Checking Search Result Model...")
        search_result_model = self.wait_and_execute(self.driver, self.search_result_model_locator, 10, lambda elem: elem.text)
        assert search_result_year==search_entries[2]
