#!/usr/bin/python3
import argparse
from webcorpcrawler import IgScraper, JsonUpdater

def main():
    parser = argparse.ArgumentParser(description='Fetches the results of a web corpus query to json')
    parser.add_argument('action', 
            metavar = 'action',
            choices = ["crawl", "add_uids"], help="The action to run")
    parser.add_argument('-c',  '--corpus',
            metavar = 'corpus name',
            choices = ["integrum"], default="integrum",
            help="Which web corpus to use")
    parser.add_argument('--files',
            metavar = "json files",
            nargs = "*",
            help="path to the folder containing the json files (produced as a result of a previous crawl) OR a list of files")
    parser.add_argument('--prettyprint',
            nargs = "?",
            const = True,
            default = False,
            help="prettyprints the json files")

    args = parser.parse_args()
    updater = None

    if args.action == "crawl":
        print("let's crawl")
    elif args.action == "add_uids":
        updater = JsonUpdater(args.files)
        updater.AddUids()

    if updater:
        updater.Output(args.prettyprint)

if __name__ == '__main__':
    main()

