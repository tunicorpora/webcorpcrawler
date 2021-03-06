#! /usr/bin/python3.6
import json
import glob
import os.path
import os
import uuid
import progressbar
import re
import sys
from webcorpcrawler.fixes import TryToFixByText
from .sentence_filter import FilterByCharCount


class JsonUpdater():
    """Updates the crawled results in various ways"""

    def __init__(self, files, corpus="integrum"):
        """
        -folder: path to folder containing json files
        """

        if not files:
            print(
                "You have to provide the target / source files of the action")
            sys.exit(2)

        self.files = []
        self.data = []
        if len(files) == 1 and os.path.isdir(files[0]):
            dirname = files[0] if files[0][-1] == "/" else files[0] + "/"
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

    def FixFakeNewLines(self, key):
        """
        fixes cases where newlines accidentally printed as literal \n
        """

        for e_idx, entry in enumerate(self.data):
            for i_idx, item in enumerate(entry["data"]):
                self.data[e_idx]["data"][i_idx][key] = re.sub(
                    r"\\n\\n", r"\n\n", self.data[e_idx]["data"][i_idx][key])

    def FixLongSentences(self, key):
        """
        fixes cases where newlines accidentally printed as literal \n
        """

        for e_idx, entry in enumerate(self.data):
            for i_idx, item in enumerate(entry["data"]):
                self.data[e_idx]["data"][i_idx][key] = FilterByCharCount(
                    self.data[e_idx]["data"][i_idx][key], item["id"])

    def AddUids(self):
        """
        Adds unique indices to crawled entries and updates the json files
        """

        print("Adding unique indices")
        for e_idx, entry in enumerate(self.data):
            for i_idx, item in enumerate(entry["data"]):
                self.data[e_idx]["data"][i_idx]["id"] = str(uuid.uuid4())

    def extractMatchContext(self, prop):
        """
        """

        splitpattern = re.compile(r"\n{2,}")
        for e_idx, entry in enumerate(self.data):
            for i_idx, item in enumerate(entry["data"]):
                match = self.data[e_idx]["data"][i_idx]["match"]
                paragraphs = splitpattern.split(
                    self.data[e_idx]["data"][i_idx][prop])
                self.data[e_idx]["data"][i_idx]["matchcontext"] = r"\n\n".join(
                    [
                        p for p in paragraphs
                        if match.replace(r"¶", r"\n\n").strip() in p
                    ])

    def PrepareForParsing(self,
                          target_prop,
                          target_dir="/tmp",
                          parsertype="default"):
        """
        Prepares some property of each item in the json for parsing using
        unique identifiers

        - target_prop:  what us the property that contains the string to be parsed
        """

        if not target_prop:
            print(
                "Please define the name of the property that the parsing will be based on"
            )
            return False

        print("Preparing...")
        ids = []
        contents = []
        for entry in self.data:
            for item in entry["data"]:
                if target_prop in item:
                    added = False
                    #Don't take into account ig the target prop is empty
                    if item[target_prop]:
                        if item[target_prop].strip():
                            ids.append(item["id"])
                            # NOTE: adjusting too long sentences
                            cleaned = FilterByCharCount(
                                item[target_prop], item["id"])
                            contents.append(cleaned)
                            added = True
                    if not added:
                        print("NOTE: the segment with the id " + item["id"] +
                              " contained an empty " + target_prop +
                              "and will not be processed")

        if parsertype == "turku_ud":
            separator_string = "\n###C:splitsegmentsbymepleasewouldyoubesokindhtankyouverymuchxdxdxd\n"
        else:
            separator = {"mark": "!", "counter": 15}
            separator_string = "\n" + separator["mark"] * separator[
                "counter"] + "\n"

        if not target_dir:
            target_dir = "/tmp"
        dirname = target_dir if target_dir[-1] == "/" else target_dir + "/"
        os.makedirs(dirname, exist_ok=True)
        with open(dirname + "contents.txt", "w") as f:
            f.write(separator_string.join(contents))
        with open(dirname + "ids.txt", "w") as f:
            f.write("\n".join(ids))
        print("The prepared files were produced at {}".format(target_dir))

    def AddParsed(self,
                  target_prop,
                  source_file,
                  index_file,
                  parsertype="default"):
        """

        - target_prop: name of the new property representing the parsed results
        - source_file: parsed results
        - index_file: file with indices
        """
        with open(source_file, "r") as f:
            raw = f.read()
        if parsertype == "default":
            splitpattern = re.compile(r"\d+\t![^\n]+\n\n?" * 14 +
                                      r"\d+\t![^\n]+\n\n")
        elif parsertype == "stanford":
            splitpattern = re.compile(r"\d+\t!{14}[^\n]+\n\n")
        elif parsertype == "turku_ud":
            separator_string = "splitsegmentsbymepleasewouldyoubesokindhtankyouverymuchxdxdxd"
            raw_old = raw
            raw = "\n".join([
                l for l in raw.splitlines()
                if not re.search("^#", l) or separator_string in l
            ])
            #TODO: use metadata.. Why only 10??
            splitpattern = re.compile(".*" + separator_string + ".*")
        results = splitpattern.split(raw)
        with open(index_file, "r") as f:
            indices = f.read().splitlines()
        if len(results) != len(indices):
            print(
                "The number of indices and parsed entries does not match: {} vs. {}"
                .format(len(results), len(indices)))
            failed = True
            if parsertype == "turku_ud":
                path = input(
                    "You can try to fix this alignment problem by providing the contents.txt file. Write the path to the file:\n>"
                )
                while not os.path.isfile(path):
                    path = input(
                        "No such file, try again. Write the path to the file:\n>"
                    )
                with open(path, "r") as f:
                    orig = f.read()
                matches = TryToFixByText(orig, raw_old)
                if (matches):
                    failed = False
                    res_by_id = {}
                    for match in matches:
                        res_by_id[indices[match["idx"]]] = match["conll"]
            if failed:
                sys.exit(0)
        else:
            failed = False
            res_by_id = {}
            for idx, res in enumerate(results):
                res_by_id[indices[idx]] = res

        if not failed:
            for e_idx, entry in enumerate(self.data):
                for i_idx, item in enumerate(entry["data"]):
                    if item["id"] in res_by_id:
                        self.data[e_idx]["data"][i_idx][
                            target_prop] = res_by_id[item["id"]]

    def Output(self, prettyprint=False):
        """
        Saves the changes made to the json files

        - prettyprint: should the json files be pretty printed
        """
        print("Updating...")
        for item in progressbar.progressbar(self.data):
            with open(item["fname"], "w") as f:
                json.dump(item["data"],
                          f,
                          ensure_ascii=False,
                          indent=4 if prettyprint else None)
        print("done.")
