from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(LiveServerTestCase):

    MAX_WAIT = 3 # max time in seconds test will wait for browser to update before throwing exception
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.1) # wait before next attempt

    def test_can_start_a_list_for_one_user(self):
        # Timmy the user checks out the app's homepage.
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy tennis balls" into a text box
        inputbox.send_keys('Buy tennis balls')

        # When he hits enter, the page updates and the page lists "1: Buy tennis balls" as an item on the to-do list.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1) # let page refresh on ENTER
        self.wait_for_row_in_list_table('1: Buy tennis balls')        

        # Another text box requests another to-do item. He enters "Play tennis".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Play tennis')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and shows both items on list
        self.wait_for_row_in_list_table('1: Buy tennis balls')        
        self.wait_for_row_in_list_table('2: Play tennis')        

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User A starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do arbitrary thing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Do arbitrary thing')        

        # User A notices their list has a unique URL
        user_A_list_url = self.browser.current_url
        self.assertRegex(user_A_list_url, '/lists/.+')

        # A new user, User B, comes to the site

        ## Create new browser session to make sure no previous information coming from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User B visits the home page. There is no sign of User A's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Do arbitrary thing', page_text)

        # User B starts their list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # User B gets their own unique URL
        user_B_list_url = self.browser.current_url
        self.assertRegex(user_B_list_url, '/lists/.+')
        self.assertNotEqual(user_A_list_url, user_B_list_url)

        # There continues to be no trace of user A's list
        page.text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Do arbitrary thing', page_text)
        self.assertIn('Buy milk', page_text)
