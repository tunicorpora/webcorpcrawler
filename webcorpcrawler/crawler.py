#! /usr/bin/python3.6

import yaml
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options
import logging
import time
import os
import json


class Scraper():
    """Scraper for automatic retrieval of data from IG"""

    def __init__(self):
        self.tasks = []
        self.browser_started = False
        self.browser = None
        self.whichbrowser = "Cromium"
        self.testmode = False
        self.data = {}
        self.injected_credentials = ''

    def SetTestmode(self):
        self.testmode = True

    def Start(self):
        """
        starts the browser

        Firefox:
            - remember to find out the right profile location
            - cf. https://stackoverflow.com/questions/52997746/selenium-crashing-with-selenium-common-exceptions-webdriverexception-message-n
        Chromium:
            - cf. https://stackoverflow.com/questions/22476112/using-chromedriver-with-selenium-python-ubuntu
            - sudo apt-get install chromium-chromedriver
            - driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
            - also relevant: https://stackoverflow.com/questions/16180428/can-selenium-webdriver-open-browser-windows-silently-in-background

        """
        loggerlocation = "crawler.log"
        logging.basicConfig(filename=loggerlocation,
                            level=logging.INFO,
                            format='%(asctime)s %(message)s')
        print("Starting. Check out the logger at " + loggerlocation)

        logging.info('Trying to start the browser')
        if self.whichbrowser == "Firefox":
            profile = FirefoxProfile(
                '/home/juho/.mozilla/firefox/thjkscy9.default/')
            self.browser = webdriver.Firefox(profile)
        else:
            chrome_options = Options()
            if not self.testmode:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("no-sandbox")
            self.browser = webdriver.Chrome(
                "/usr/lib/chromium-browser/chromedriver",
                options=chrome_options)
        self.browser.implicitly_wait(3)
        self.browser_started = True
        logging.info('Browser started')

    def GetTaskFromYaml(self, yamlpath):
        """
        Format the yaml as follows: 

        targets: 
            - url: http://aaaa
              meta: testi
            - url: http://aaaa
              meta: testi

        """
        with open(yamlpath, "r") as f:
            targets = yaml.safe_load(f)

        for target in targets["targets"]:
            self.tasks.append(target)
            self.data[target["meta"]] = []

        self.output_folder = targets["output"]

    def Get(self, url):
        """
        Gets a page
        """
        if self.injected_credentials:
            url = url.replace('https://',
                              'https://{}'.format(self.injected_credentials))
            url = url.replace('http://',
                              'http://{}'.format(self.injected_credentials))
        logging.info("Getting url: " + url)
        self.browser.get(url)
        time.sleep(1)

    def Stop(self):
        """
        Gracefully shut down
        """
        logging.info("Quitting...")
        if self.browser_started:
            if self.browser:
                if not self.testmode:
                    self.browser.quit()
                    logging.info("The browser window was closed.")
        if self.data:
            self.Output()

    def Crawl(self):
        """
            Does some crawling and cleans up if something goes wrong
        """
        if not self.browser_started:
            self.Start()

        try:
            for task in self.tasks:
                logging.info("Running the crawler's tasks for " + task["meta"])
                self.Run(task)
                logging.info("task finished")
        except KeyboardInterrupt:
            self.Stop()
        finally:
            self.Stop()

    def Output(self):
        """ 
        outputs the data according to the default folder structure given in the yaml config file
        """
        for taskid, taskdata in self.data.items():
            logging.info(taskid)
            root = self.output_folder[0]["root"]
            fn = "{}/{}.json".format(root, taskid)
            logging.info("Outputting the data to: " + fn)
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'w') as fp:
                json.dump(taskdata, fp, ensure_ascii=False)
        logging.info("Outputting done.")
