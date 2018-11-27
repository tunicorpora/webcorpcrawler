#! /usr/bin/python3.6

import json
import glob
import os.path
import uuid
import progressbar


class JsonUpdater():
    """Updates the crawled results in various ways"""

    def __init__(self, files, corpus="integrum"):
        """
        -folder: path to folder containing json files
        """

        self.files = []
        self.data = []
        if len(files) == 1 and os.path.isdir(files[0]):
            dirname = files[0] if files[0][-1] == "/"  else files[0] + "/"
            for fname in glob.glob(dirname + "*.json"):
                self.files.append(fname)
        else:
            self.files = files


    def AddUids(self):
        """
        Adds unique indices to crawled entries and updates the json files
        """
        print("indexing files...")
        for fname in progressbar.progressbar(self.files):
            with open(fname, "r") as f:
                data = json.load(f)
            for idx, item in enumerate(data):
                data[idx]["id"] = str(uuid.uuid4())
            self.data.append({"data": data, "fname": fname})


    def Output(self, prettyprint=False):
        """
        Saves the changes made to the json files

        - prettyprint: should the json files be pretty printed
        """
        print("Updating...")
        for item in progressbar.progressbar(self.data):
            with open(item["fname"], "w") as f:
                json.dump(item["data"], f,
                        ensure_ascii=False,
                        indent=4 if prettyprint else None)
        print("done.")



