#!/usr/bin/python3
import argparse
from webcorpcrawler import IgScraper, JsonUpdater

def main():
    parser = argparse.ArgumentParser(description='Fetches the results of a web corpus query to json')
    parser.add_argument('action', 
            metavar = 'action',
            choices = ["crawl", "add_uids", "prepare", "add_parsed", "custom"], help="The action to run")
    parser.add_argument('-c',  '--corpus',
            metavar = 'corpus name',
            choices = ["integrum"], default="integrum",
            help="Which web corpus to use")
    parser.add_argument('--files',
            metavar = "json files",
            nargs = "*",
            help="path to the folder containing the json files (produced as a result of a previous crawl) OR a list of files")
    parser.add_argument('--crawlconfig',
            metavar = "path to yaml file",
            help="a yaml file containing what to parse. For examples see the scripts repository")
    parser.add_argument('--prop',
            metavar = "property name",
            help="which property of a data item (concordance) will be used in the action")
    parser.add_argument('--indices',
            metavar = "path",
            help="path to the file containing indices, produced by the 'prepare' action")
    parser.add_argument('--output_folder',
            metavar = "path to folder",
            help="where to put the output files")
    parser.add_argument('--parsed_source',
            metavar = "path",
            help="path to a file containing the parsed results")
    parser.add_argument('--parser',
            metavar = "parser name",
            default = "default",
            help="The name of the parser that was used")
    parser.add_argument('--prettyprint',
            nargs = "?",
            const = True,
            default = False,
            help="prettyprints the json files")
    parser.add_argument('--actionfile',
            metavar = "filename",
            default = "default",
            help="Path to the file containing the custom action")

    args = parser.parse_args()

    if args.action == "crawl":
        if args.corpus == "integrum":
            s = IgScraper()
            s.GetTaskFromYaml(args.crawlconfig)
            s.Crawl()
    elif args.action == "add_uids":
        updater = JsonUpdater(args.files)
        updater.AddUids()
        updater.Output(args.prettyprint)
    elif args.action == "prepare":
        updater = JsonUpdater(args.files)
        updater.PrepareForParsing(args.prop, args.output_folder)
    elif args.action == "add_parsed":
        updater = JsonUpdater(args.files)
        updater.AddParsed(args.prop, args.parsed_source, args.indices, args.parser)
        updater.Output(args.prettyprint)
    elif args.action == "custom":
        with open(args.actionfile, "r") as f:
            code = f.read()
        exec(code)
        updater = JsonUpdater(args.files)
        updater.custom(args)


if __name__ == '__main__':
    main()

