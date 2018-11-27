#! /usr/bin/python3.6

import json
import glob
import os.path


class Indexer():
    """Adds unique indices to json objects"""

    def __init__(self, files):
        """
        -folder: path to folder containing json files
        """

        self.files = []
        if len(files) == 1 and os.path.isdir(files[0]):
            dirname = files[0] if files[0][-1] == "/"  else files[0] + "/"
            for fname in glob.glob(dirname + "*.json"):
                self.files.append(fname)
        else:
            self.files = files

        print(self.files)

    def ReadFiles(self):
        path = os.path.abspath(self.folder)
        #if not os.path.isdir(path):
        #    print("not a dir")
        #else:
        #    print()
        #    sys.exit(2)
        print()
        #for fname in glob.glob(self.folder):
        #    print (fname)




