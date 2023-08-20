import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


LOG = logging.getLogger(__name__)


class Browser:


    def __init__(self, browser_loc):

        self.driver = self.make_browser(browser_loc)


    def make_browser(self, browser_loc):
        """ Make browser with provided path to installed browser """

        service = Service(browser_loc)
        options = Options()
        driver = webdriver.Chrome(service=service, options=options)        
        return driver


    def open(self, url):
        """ Open targeted URL. """

        self.driver.get(url)


    def get_elements(self, xpath):
        """ Get selected elements. """

        return self.driver.find_elements(By.XPATH, xpath)


    def get_element(self, xpath):
        """ Get selected element. """

        return self.driver.find_element(By.XPATH, xpath)


    def quit(self):
        """ Exit browser. """

        self.driver.quit()
