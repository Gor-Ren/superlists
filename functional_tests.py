from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Timmy the user checks out the app's homepage.
        self.browser.get('http://localhost:8000')

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
        self.check_for_row_in_list_table('1: Buy tennis balls')        

        # Another text box requests another to-do item. He enters "Play tennis".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Play tennis')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and shows both items on list
        self.check_for_row_in_list_table('1: Buy tennis balls')        
        self.check_for_row_in_list_table('2: Play tennis')        

        # Timmy wonders whether the site will remember his list. Then he sees that the site has generated a unique URL for him
        # -- there is some explanatory text to that effect
        self.fail('Finish the test!')

        # He visits the URL - his to-do list is still there

        # Satisfied, he closes his browser

if __name__ == '__main__':
    unittest.main(warnings='ignore')
