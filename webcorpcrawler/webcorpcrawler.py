#!/usr/bin/python3
import argparse
from webcorpcrawler import IgScraper, Indexer

def main():
    parser = argparse.ArgumentParser(description='Fetches the results of a web corpus query to json')
    parser.add_argument('action', 
            metavar = 'action',
            choices = ["crawl", "index"], help="The command to run")
    parser.add_argument('-c',  '--corpus',
            metavar = 'corpus name',
            choices = ["integrum"], default="integrum",
            help="Which web corpus to use")
    parser.add_argument('--files',
            metavar = "json files",
            nargs = "*",
            help="path to the folder containing the json files (produced as a result of a previous crawl) OR list of files")

    args = parser.parse_args()
    if args.action == "crawl":
        print("let's crawl")
    if args.action == "index":
        indexer = Indexer(args.files)
        #indexer.ReadFiles()

if __name__ == '__main__':
    main()

