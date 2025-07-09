#!/usr/bin/env python3
#
# PHP source code grep tool
# bl4de | github.com/bl4de | hackerone.com/bl4de
#

# pylint: disable=invalid-name, missing-class-docstring, import-error, too-few-public-methods, unused-import, no-self-use,missing-function-docstring,consider-using-enumerate,consider-iterating-dictionary

# @TODO:
# - allow to scan folder without subdirs
# - allow to scan files by pattern, eg. *.php
# - exclude 'echo' lines without HTML tags

## Sinks and Sources
#
# for an SQLi, you need a code that makes a raw query to the database
# for an SSRF, you need a code that makes an HTTP request
# for an LFI, you need a code that reads a file
# for an XXE, you need a code that parses an XML with a concrete configuration
# for a DOM-XSS, you need a code that executes HTML or JavaScript
#
# When you are going sources to sinks, the process is:
#
# - you encounter a function call
# - you find the definition
# - repeat until the sink
#
# For sinks to sources, the process is:
#
# - you are in the function definition
# - you find a call of this function.
# - repeat until the source
#

import argparse
import os
import re
import sys

from imports.pefdocs import exploitableFunctions, exploitableFunctionsDesc
from imports.beautyConsole import beautyConsole

# allowed scan levels
ALLOWED_LEVELS = ['ALL', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
DEFAULT_LEVELS = 'MEDIUM,HIGH,CRITICAL'

ALLOWED_LANG = ['PHP', 'JavaScript']
DEFAULT_LANG = 'PHP'

class PefEngine:
    """
    implements pef engine
    """

    def __init__(self, lang, level, source_or_sink, filename, skip_vendor, phpfunction, verbose):
        """
        constructor
        """
        self.lang = lang # selected language
        self.level = level  # scan only for level set of functions
        self.source_or_sink = source_or_sink  # show only sinks or sources
        self.filename = filename  # name of file/folder to scan
        self.skip_vendor = skip_vendor
        self.phpfunction = '' if phpfunction is None else phpfunction
        self.verbose = verbose
        self.scanned_files = 0  # number of scanned files in total
        self.found_entries = 0  # total number of findings

        self.severity = {  # severity scale
            "high": 0,
            "medium": 0,
            "low": 0
        }

        self.header_printed = False
        return

    def analyse_line(self, l, i, fn, f, line):
        """
        analysis of single line of code; searches for pattern (passed as fn and atfn) occurence

        if occurence found, output is printed
        """
        total_number_of_isses = None
        meets_criteria = 0

        if fn in line:
            if fn == "`":
                total_number_of_isses = self.print_code_line(
                    f.name, l, i, fn, self.severity, self.level, self.source_or_sink)
            else:
                total_number_of_isses = self.print_code_line(
                    f.name, l, i, fn + (')' if '(' in fn else ''), self.severity, self.level,
                    self.source_or_sink)
            meets_criteria = meets_criteria + 1 if total_number_of_isses is not None else meets_criteria
        return (meets_criteria, total_number_of_isses)

    def print_code_line(self, file_name, _line, i, fn, severity="", level='ALL', source_or_sink='ALL'):
        """
        prints formatted code line
        """
        impact_color = {
            "low": "grey",
            "medium": "green",
            "high": "yellow",
            "critical": "red"
        }

        meets_criteria = 0
        # print legend only if there is entry in pefdocs.py

        if fn and fn.strip() in exploitableFunctionsDesc[self.lang].keys():
            doc = exploitableFunctionsDesc[self.lang].get(fn.strip())
            impact = doc[3]

            if (impact.upper() in level.upper()) or level == 'ALL':
                if self.phpfunction == '' or self.phpfunction in fn:
                    if (len(doc) == 5 and source_or_sink == doc[4]) or source_or_sink == 'ALL':
                        if len(_line) > 255:
                            _line = _line[:120] + \
                                    f" (...truncated -> line is {len(_line)} characters long)"
                        print("{}{}:{}\t{}{}{}{}".format(beautyConsole.getColor("white"), file_name, i,
                                                         beautyConsole.getColor(
                                                             impact_color[impact]),
                                                         beautyConsole.getColor(impact_color[impact]),
                                                         _line.strip()[:255],
                                                         beautyConsole.getColor("grey")))
                        if self.verbose:
                            print(f"\t{doc[1]}\n\t{doc[0]}\n")
                        meets_criteria += 1
            if impact not in severity.keys():
                severity[impact] = 1
            else:
                severity[impact] = severity[impact] + 1
            return meets_criteria

    def main(self, src):
        """
        main engine loop
        """
        f = open(str(src), "r", encoding="ISO-8859-1")
        i = 0
        res = None
        file_found = 0
        all_lines = f.readlines()
        for l in all_lines:
            i += 1
            line = l.rstrip()
            if self.level:
                if not self.is_comment(line):
                    for fn in exploitableFunctions[self.lang]:
                        (meets_criteria, number_of_issues) = self.analyse_line(l, i, fn, f, line)
                        if number_of_issues is not None:
                            res = True
                            file_found += number_of_issues
        return (res, file_found)  # return how many findings in current file

    def run(self):
        """
        runs scanning
        """
        total_found = 0

        print(
            f"{beautyConsole.getColor('green')}>>> RESULTS <<<{beautyConsole.getColor('gray')}\n")

        if os.path.isdir(str(self.filename)):
            for root, _, files in os.walk(self.filename):
                if self.skip_vendor is True and "vendor" in root:
                    continue
                for f in files:
                    extension = f.split('.')[-1:][0]
                    if extension in ['php', 'inc', 'php3', 'php4', 'php5', 'phtml']:
                        self.scanned_files = self.scanned_files + 1
                        (res, file_found) = self.main(os.path.join(root, f))
                        if file_found > 0:
                            print(f">>> {f} <<<\t{'-' * (115 - len(f))}\n")
                        total_found += file_found
        else:
            self.scanned_files = self.scanned_files + 1
            (res, total_found) = self.main(self.filename)
        # print summary
        self.print_summary(total_found)

    def is_comment(self, line: str) -> bool:
        """
        If line is a comment, we should ignore it
        """
        line = re.sub(r"\s+", "", line)
        return line.startswith("/") or line.startswith("*")

    def print_summary(self, total_found: int) -> None:
        """
        prints summary at the bottom of search results
        """
        print(f"{beautyConsole.getColor('white')}Patterns found: {total_found}")
        print(f"\n{beautyConsole.getColor('grey')}Cmd arguments: {' '.join(sys.argv[1:])}")
        print(f"{beautyConsole.getColor('grey')}Severity levels: {beautyConsole.getColor('grey')} LOW {beautyConsole.getColor('green')} MEDIUM {beautyConsole.getColor('yellow')} HIGH {beautyConsole.getColor('red')} CRITICAL{beautyConsole.getColor('grey')}\n")


def banner():
    """
    Prints welcome banner with contact info
    """
    print(beautyConsole.getColor("green") + "\n\n", "-" * 100)
    print("-" * 6, " PEF | PHP Source Code grep tool",
          " " * 35, "-" * 16)
    print("-" * 6, " https://github.com/bl4de ",
          " " * 22, "-" * 16)
    print("-" * 100, "\33[0m\n")

def parse_arguments():
    """
    Parses command line arguments
    """
    parser = argparse.ArgumentParser(
        description="PHP Source Code grep tool",
        add_help=True
    )
    parser.add_argument(
        "-s", "--skip-vendor", help="exclude ./vendor folder", action="store_true")
    parser.add_argument(
        "-v", "--verbose", help="show documentation", action="store_true")
    parser.add_argument(
        "-l", "--level",
        help=f"severity: ALL, LOW, MEDIUM, HIGH or CRITICAL; default: {DEFAULT_LEVELS}")
    parser.add_argument(
        "-L", "--lang",
        help=f"language: PHP, JavaScript; default: {DEFAULT_LANG}")
    parser.add_argument(
        "-S", "--sources", help="show only sources", action="store_true")
    parser.add_argument(
        "-K", "--sinks", help="show only sinks", action="store_true")
    parser.add_argument(
        "-f",
        "--function",
        help="Search for particular PHP function (eg. unserialize)",
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="Directory to scan (or single file, optionally)",
    )
    return parser.parse_args()

# main program
if __name__ == "__main__":

    if len(sys.argv) == 1:
        print(f"{beautyConsole.getColor('red')}No arguments provided, use -h for help")
        exit(1)

    args = parse_arguments()

    lang = args.lang.lower() if args.lang else DEFAULT_LANG.lower()
    level = args.level.upper() if args.level else 'HIGH,CRITICAL'

    # if we are looking for a specific function, level is not taken into account
    if args.function is not None:
        level = 'ALL'
    source_or_sink = 'ALL'

    if args.sources:
        source_or_sink = 'source'
    if args.sinks:
        source_or_sink = 'sink'

    # if no directory or file is provided, exit
    if args.dir is None:
        print(f"{beautyConsole.getColor('red')}No directory or file(s) to scan provided...")
        exit(1)

    # check if the langauge selected is available
    if lang not in [l.lower() for l in ALLOWED_LANG]:
        print(f"{beautyConsole.getColor('red')}Language {args.lang} is not supported, use one of: {', '.join(ALLOWED_LANG)}")
        exit(1)

    filename = args.dir

    # main orutine starts here
    engine = PefEngine(lang, level, source_or_sink,
                       filename, args.skip_vendor, args.function, args.verbose)
    engine.run()
