import unittest
from selenium import webdriver
from historymap.urls import urlpatterns
from time import sleep

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_land_page_is_okay(self):
        self.browser.get('http://localhost:8000')
        #sleep(40)
        self.assertIn('HistoryMap', self.browser.title)
        #self.fail('Finish the Test')

"""
def _get_reversed_urlpatterns(urlspatterns=urlpatterns):
    Yields list of urls in website
    return False
"""

if __name__ == '__main__':
    unittest.main(warnings='ignore')

