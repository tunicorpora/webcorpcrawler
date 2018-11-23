from crawler import Scraper
import logging
import subprocess

class IgScraper(Scraper):

    def __init__(self):
        super().__init__()

    def LibLogin(self):
        """
        Log in to uta library
        """
        logging.info("Trying to make a login.. ")
        self.browser.find_element_by_css_selector('.shibboleth-login a').click()
        self.browser.find_element_by_css_selector('#username').send_keys(self.ReadUname())
        self.browser.find_element_by_css_selector('#password').send_keys(self.ReadPassword())


    def ReadPassword(self):
        """
        Reads user credentials from password store
        """
        return subprocess.check_output([ "pass", "show", "essential/yo" ]).decode("utf-8")

    def ReadUname(self):
        """
        Reads user credentials from password store
        """
        return subprocess.check_output([ "pass", "show", "essential/yo_uname" ]).decode("utf-8")


    def Run(self, url):
        """
        What this crawler does...
        """
        self.Get(url)
        self.LibLogin()

        #shibboleth-login
