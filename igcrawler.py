from crawler import Scraper
import logging
import subprocess
from bs4 import BeautifulSoup
import os.path
import json
import selenium
import justext
import sys
import re

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
        try:
            self.browser.find_element_by_css_selector('.shibboleth-login a').click()
            self.browser.find_element_by_css_selector('#username').send_keys(self.ReadUname())
            self.browser.find_element_by_css_selector('#password').send_keys(self.ReadPassword())
        except  selenium.common.exceptions.NoSuchElementException:
            logging.info("Already logged in?")



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
        self.browser.get(listurl)

    def NextPage(self):
        """
        Gets the next page of results as long as there is one.
        """
        try:
            nextlink = self.browser.find_element_by_xpath("//*[contains(text(), '>>')]")
            nextlink.click()
        except  selenium.common.exceptions.NoSuchElementException:
            return False

        return True


    def ProcessDocument(self, soup, taskid):
        """
        - soup: bs4 object
        """
        alltext = soup.findAll('pre')
        if alltext:
            paragraphs_raw = alltext
        else:
            paragraphs_raw = justext.justext(str(soup), justext.get_stoplist('Russian'))

        highlighted = soup.select('#f1')
        match = ""
        date = ""
        if highlighted:
            match = "".join([tag.text for tag in highlighted])

        metadata = paragraphs_raw[0].text
        if metadata:
            datematch = re.search("Дата выпуска: (.*)", metadata)
            date = datematch.group(1).strip()
            if date:
                year = re.sub("(\d+\\.)+","",date)

        self.data[taskid].append(
                {
                "meta": metadata,
                "txt":"\n\n".join([tag.text for tag in paragraphs_raw[1:]]),
                "match": match,
                "date": date,
                "year": year
                }
                )


    def Run(self, task):
        """
        What this crawler does...
        """
        pages_retrieved = 1
        self.Get(task["url"])
        self.LibLogin()
        self.GetDocuments(task["meta"])
        while self.NextPage():
            pages_retrieved += 1
            logging.info("Moved to result page number {}".format(pages_retrieved))
            self.GetDocuments(task["meta"])

if __name__ == "__main__":
    s = IgScraper()
    s.GetTaskFromYaml(sys.argv[1])
    s.Crawl()


