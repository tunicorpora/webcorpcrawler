#! /usr/bin/python3.6

import json
import glob
import os.path
import os
import uuid
import progressbar
import re
import sys


class JsonUpdater():
    """Updates the crawled results in various ways"""

    def __init__(self, files, corpus="integrum"):
        """
        -folder: path to folder containing json files
        """

        if not files:
            print("You have to provide the target / source files of the action")
            sys.exit(2)

        self.files = []
        self.data = []
        if len(files) == 1 and os.path.isdir(files[0]):
            dirname = files[0] if files[0][-1] == "/"  else files[0] + "/"
            for fname in glob.glob(dirname + "*.json"):
                self.files.append(fname)
        else:
            self.files = files
        self.ReadData()


    def ReadData(self):
        """
        Reads the json files to memory
        """
        print("Reading files...")
        for fname in progressbar.progressbar(self.files):
            with open(fname, "r") as f:
                data = json.load(f)
                self.data.append({"data": data, "fname": fname})

    def AddUids(self):
        """
        Adds unique indices to crawled entries and updates the json files
        """

        print("Adding unique indices")
        for e_idx, entry in enumerate(self.data):
            for i_idx, item in enumerate(entry["data"]):
                self.data[e_idx]["data"][i_idx]["id"] = str(uuid.uuid4())

    def PrepareForParsing(self, target_prop, target_dir="/tmp"):
        """
        Prepares some property of each item in the json for parsing using
        unique identifiers

        - target_prop:  what us the property that contains the string to be parsed
        """

        if not target_prop:
            print("Please define the name of the property that the parsing will be based on")
            return False

        print("Preparing...")
        ids = []
        contents = []
        for entry in self.data:
            for item in entry["data"]:
                if target_prop in item:
                    ids.append(item["id"])
                    contents.append(item[target_prop])

        separator = {"mark" : "!", "counter" : 15}
        separator_string = "\n" + separator["mark"] * separator["counter"] + "\n"

        if not target_dir:
            target_dir = "/tmp"
        dirname = target_dir if target_dir[-1] == "/"  else target_dir + "/"
        os.makedirs(dirname, exist_ok=True)
        with open(dirname + "contents.txt","w") as f:
            f.write(separator_string.join(contents))
        with open(dirname + "ids.txt","w") as f:
            f.write("\n".join(ids))
        print("The prepared files were produced at {}".format(target_dir))

    def AddParsed(self, target_prop, source_file, index_file):
        """

        - target_prop: name of the new property representing the parsed results
        - source_file: parsed results
        - index_file: file with indices
        """
        with open(source_file, "r") as f:
            raw = f.read()
        splitpattern = re.compile(r"\d+\t![^\n]+\n\n?"*14 + r"\d+\t![^\n]+\n\n")
        results = splitpattern.split(raw)
        with open(index_file, "r") as f:
            indices = f.read().splitlines()
        if len(results) != len(indices):
            print("The number of indices and parsed entries does not match: {} vs. {}"
                    .format(len(results), len(indices)))
            sys.exit(0)
        else:
            res_by_id = {}
            for idx, res in enumerate(results):
                res_by_id[indices[idx]] = res
            for e_idx, entry in enumerate(self.data):
                for i_idx, item in enumerate(entry["data"]):
                    if item["id"] in res_by_id:
                        self.data[e_idx]["data"][i_idx][target_prop] = res_by_id[item["id"]]


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



