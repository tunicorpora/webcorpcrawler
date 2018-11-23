import unittest
import re
from pandoc_avm import Texconstruction, ParseConstruction, NodeGroup, Nobox
from crawler import Scraper
from igcrawler import IgScraper
import bs4

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
        #self._scraper.SetTestmode()
        self._scraper.Crawl()

    def test_readpw(self):
        self._scraper.ReadPassword()
        self._scraper.ReadUname()

    def test_folders(self):
        self._scraper.GetTaskFromYaml(self._yamlpath)

    def test_process_document(self):
        return 0
        with open("testdata/document.html","r") as f:
            test = f.read()
        soup = bs4.BeautifulSoup(test,'lxml')
        self._scraper.ProcessDocument(soup, "testi")
        self._scraper.Output()



if __name__ == '__main__':
    unittest.main()



