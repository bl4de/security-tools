#!/usr/bin/env python3
#
# PHP Exploitable Functions/Vars Scanner
# bl4de | github.com/bl4de | hackerone.com/bl4de
#

# pylint: disable=C0103

# //TODO:
# - allow to scan folder without subdirs
# - allow to scan files by pattern, eg. *.php
# - exclude 'echo' lines without HTML tags


"""
pef.py - PHP source code advanced grep utility
"""
import sys
import os
import re
import argparse

from imports import pefdefs
from imports import pefdocs
from imports.beautyConsole import beautyConsole


def banner():
    """
    Prints welcome banner with contact info
    """
    print(beautyConsole.getColor("green") + "\n\n", "-" * 100)
    print("-" * 6, " PEF | PHP Exploitable Functions source code advanced grep utility",
          " " * 35, "-" * 16)
    print("-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ",
          " " * 22, "-" * 16)
    print("-" * 100, "\33[0m\n")


class PefEngine:
    """
    implements pef engine
    """

    def __init__(self, recursive, level, filename):
        """
        constructor
        """
        self.recursive = recursive  # recursive scan files in folder(s)
        self.level = level          # scan only for level set of functions
        self.filename = filename    # name of file/folder to scan

        self.scanned_files = 0    # number of scanned files in total
        self.found_entries = 0    # total number of findings

        self.severity = {         # severity scale
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

        # there has to be space before function call; prevents from false-positives strings contains PHP function names
        atfn = "@{}".format(fn)
        fn = "{}".format(fn)
        # also, it has to checked agains @ at the beginning of the function name
        # @ prevents from output being echoed

        if fn in line or atfn in line:
            self.print_code_line(f.name, l, i, fn + (')' if '(' in fn else ''), self.severity,
                                 self.level)
        return

    def print_code_line(self, file_name, _line, i, fn, severity="", level='ALL'):
        """
        prints formatted code line
        """
        impact_color = {
            "low": "green",
            "medium": "yellow",
            "high": "red",
            "critical": "red"
        }

        # print legend only if there i sentry in pefdocs.py
        if fn and fn.strip() in pefdocs.exploitableFunctionsDesc.keys():
            impact = pefdocs.exploitableFunctionsDesc.get(fn.strip())[3]
            vuln_class = pefdocs.exploitableFunctionsDesc.get(fn.strip())[2]

            if impact.upper() == level.upper() or level == 'ALL':
                if len(_line) > 255:
                    _line = _line[:120] + \
                        f" (...truncated -> line is {len(_line)} characters long)"
                else:
                    print("{}{}:{}{} -> {}{}".format(beautyConsole.getColor(
                        "white"), file_name, i, beautyConsole.getColor(impact_color[impact]), _line.strip()[:255], beautyConsole.getColor("grey"), vuln_class))

            if impact not in severity.keys():
                severity[impact] = 1
            else:
                severity[impact] = severity[impact] + 1
            return

    def main(self, src):
        """
        main engine loop
        """
        f = open(src, "r", encoding="ISO-8859-1")
        i = 0
        all_lines = f.readlines()

        for l in all_lines:
            i += 1
            line = l.rstrip()
            if self.level:
                for fn in pefdefs.exploitableFunctions:
                    self.analyse_line(l, i, fn, f, line)

        return  # return how many findings in current file

    def run(self):
        """
        runs scanning
        """
        if self.recursive:
            for root, subdirs, files in os.walk(self.filename):
                for f in files:
                    extension = f.split('.')[-1:][0]
                    if extension in ['php', 'inc', 'php3', 'php4', 'php5', 'phtml']:
                        self.scanned_files = self.scanned_files + 1
                        res = self.main(os.path.join(root, f))
        else:
            self.scanned_files = self.scanned_files + 1
            self.found_entries = self.main(self.filename)

        print(beautyConsole.getColor("white") + "-" * 100)
        print("\n")


# main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__
    )
    filename = '.'  # initial value for file/dir to scan is current directory

    parser.add_argument(
        "-r", "--recursive", help="scan PHP files recursively in directory pointed by -f/--file", action="store_true")
    parser.add_argument(
        "-l", "--level", help="severity level: ALL, LOW, MEDIUM or level; default - ALL")
    parser.add_argument(
        "-f", "--file", help="File or directory name to scan (if directory name is provided, make sure -r/--recursive is set)")
    args = parser.parse_args()

    level = args.level.upper() if args.level else 'ALL'
    filename = args.file

    # main orutine starts here
    engine = PefEngine(args.recursive, level, filename)
    engine.run()
