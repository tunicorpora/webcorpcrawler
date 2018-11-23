import unittest
import re
from pandoc_avm import Texconstruction, ParseConstruction, NodeGroup, Nobox
from crawler import Scraper
from igcrawler import IgScraper


#import bs4

class CrawlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._yamlpath = "test.yml" 
        cls._scraper = IgScraper()

    def test_read_yaml(self):

        s = IgScraper()
        s.GetTaskFromYaml(self._yamlpath)

    def test_crawl(self):
        self._scraper.GetTaskFromYaml(self._yamlpath)
        self._scraper.SetTestmode()
        self._scraper.Crawl()

    def test_readpw(self):
        self._scraper.ReadPassword()
        self._scraper.ReadUname()


if __name__ == '__main__':
    unittest.main()



