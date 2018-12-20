import unittest
from webcorpcrawler import TryToFixByText

class UpdaterTest(unittest.TestCase):


    def test_read_yaml(self):
        with open("testdata/c1.txt", "r") as f:
            orig = f.read()
        with open("testdata/c2.txt", "r") as f:
            conll = f.read()
        TryToFixByText(orig, conll)


if __name__ == '__main__':
    unittest.main()



