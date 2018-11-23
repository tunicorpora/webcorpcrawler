from crawler import Scraper
import logging
import subprocess
from bs4 import BeautifulSoup
import os.path
import json

class IgScraper(Scraper):
    """
    Saving reasonable results from queries to integrum
    Instructions:
        - make the query
        - on the result page, click  "Titles"
        - get the address of the results page

    """

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

    def GetDocuments(self, taskid):
        """
        Gets the individual documents on a listing page
        """
        doculinks = self.browser.find_elements_by_css_selector('.aftitle')
        hrefs = [el.get_attribute("href") for el in doculinks]
        listurl = self.browser.current_url
        for idx, href in enumerate(hrefs):
            logging.info("Retrieving document number {}".format(idx))
            self.browser.get(href)
            self.browser.switch_to_frame("fb")
            soup = BeautifulSoup(self.browser.page_source,'lxml')
            self.ProcessDocument(soup, taskid)

    def ProcessDocument(self, soup, taskid):
        """
        - soup: bs4 object
        """
        alltext = soup.findAll('pre')
        if alltext:
            self.data[taskid].append(
                    {
                    "meta":alltext[0].text,
                    "txt":"\n\n".join([tag.text for tag in alltext[1:]])
                    }
                    )


    def Run(self, task):
        """
        What this crawler does...
        """
        self.Get(task["url"])
        self.LibLogin()
        self.GetDocuments(task["meta"])

        #shibboleth-login
