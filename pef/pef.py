#!/usr/bin/python
#
# PHP Exploitable Functions/Vars Scanner
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#

# pylint: disable=C0103
"""
pef.py - PHP static code analysis tool (very, very simple)
by bl4de
GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com
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
    print beautyConsole.getColor("green") + "\n\n", "-" * 100
    print "-" * 6, " PEF | PHP Exploitable Functions scanner", " " * 35, "-" * 16
    print "-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ", " " * 22, "-" * 16
    print "-" * 100, "\33[0m\n"


class PefEngine:
    """
    implements pef engine
    """

    def __init__(self, recursive, verbose, critical, sql, filename):
        """
        constructor
        """
        self.recursive = recursive  # recursive scan files in folder(s)
        self.verbose = verbose      # show prev/next lines
        self.critical = critical    # scan only for critical set of functions
        self.sql = sql              # scan for inline SQL queries
        self.filename = filename    # name of file/folder to scan

        self.scanned_files = 0    # number of scanned files in total
        self.found_entries = 0    # total number of findings

        self.severity = {         # severity scale
            "high": 0,
            "medium": 0,
            "low": 0
        }
        return

    def header_print(self):
        """
        prints file header
        """
        return

    def printcodeline(self):
        """
        prints formatted code line
        """
        return

    def main(self):
        """
        main engine loop
        """
        return

    def run(self):
        """
        runs scanning
        """
        if self.recursive:
            for root, subdirs, files in os.walk(self.filename):
                for f in files:
                    self.scanned_files = self.scanned_files + 1
                    res = main(os.path.join(root, f), __severity,

                               verbose, sql, critical)
                    self.found_entries = self.found_entries + res
        else:
            self.scanned_files = self.scanned_files + 1
            self.found_entries = main(self.filename, __severity)
        return


def printcodeline(_line, i, fn, prev_line="", next_line="", prev_prev_line="", next_next_line="", severity={}, verbose=False):
    """
    Formats and prints line of output
    """
    impact_color = {
        "low": "green",
        "medium": "yellow",
        "high": "red"
    }

    if verbose == True:
        print " line %d :: \33[33;1m%s\33[0m " % (i, fn)
    else:
        print "{}line {} :: {}{} ".format(beautyConsole.getColor(
            "white"), i, beautyConsole.getColor("grey"), _line.strip())

    # print legend only if there i sentry in pefdocs.py
    if fn and fn.strip() in pefdocs.exploitableFunctionsDesc.keys():
        impact = pefdocs.exploitableFunctionsDesc.get(fn.strip())[3]
        description = pefdocs.exploitableFunctionsDesc.get(fn.strip())[
            0]
        syntax = pefdocs.exploitableFunctionsDesc.get(fn.strip())[1]
        vuln_class = pefdocs.exploitableFunctionsDesc.get(fn.strip())[2]

        if verbose == True:
            print "\n  {}{}{}".format(beautyConsole.getColor(
                "white"), description, beautyConsole.getSpecialChar("endline"))
            print "  {}{}{}".format(beautyConsole.getColor(
                "grey"), syntax, beautyConsole.getSpecialChar("endline"))
            print "  Potential impact: {}{}{}".format(beautyConsole.getColor(
                impact_color[impact]), vuln_class, beautyConsole.getSpecialChar("endline"))

        if impact not in severity.keys():
            severity[impact] = 1
        else:
            severity[impact] = severity[impact] + 1

    if verbose == True:
        print "\n"
        if prev_prev_line:
            print str(i-2) + "  " + beautyConsole.getColor("grey") + prev_prev_line + \
                beautyConsole.getSpecialChar("endline")
        if prev_line:
            print str(i-1) + "  " + beautyConsole.getColor("grey") + prev_line + \
                beautyConsole.getSpecialChar("endline")
        print str(i) + "  " + beautyConsole.getColor("green") + _line.rstrip() + \
            beautyConsole.getSpecialChar("endline")
        if next_line:
            print str(i+1) + "  " + beautyConsole.getColor("grey") + next_line + \
                beautyConsole.getSpecialChar("endline")
        if next_next_line:
            print str(i+2) + "  " + beautyConsole.getColor("grey") + next_next_line + \
                beautyConsole.getSpecialChar("endline")
        print "\n"


def header_print(file_name, header_printed):
    if header_printed == False:
        print beautyConsole.getColor("white") + "-" * 100
        print "FILE: \33[33m%s\33[0m " % os.path.realpath(file_name), "\n"
        header_printed = True
    return header_printed


def main(src, severity, verbose=False, sql=False, critical=False):
    """
    performs code analysis, line by line
    """
    f = open(src, "r")
    i = 0
    total = 0
    filenamelength = len(src)
    linelength = 97
    all_lines = f.readlines()

    header_printed = False
    prev_prev_line = ""
    prev_line = ""
    next_line = ""
    next_next_line = ""

    for l in all_lines:
        if i > 2:
            prev_prev_line = all_lines[i - 2].rstrip()
        if i > 1:
            prev_line = all_lines[i - 1].rstrip()
        if i < (len(all_lines) - 1):
            next_line = all_lines[i + 1].rstrip()
        if i < (len(all_lines) - 2):
            next_next_line = all_lines[i + 2].rstrip()

        i += 1
        line = l.rstrip()

        if critical:
            for fn in pefdefs.critical:
                # there has to be space before function call; prevents from false-positives strings contains PHP function names
                atfn = "@{}".format(fn)
                fn = " {}".format(fn)
                # also, it has to checked agains @ at the beginning of the function name
                # @ prevents from output being echoed
                if fn in line or atfn in line:
                    header_printed = header_print(f.name, header_printed)
                    total += 1
                    printcodeline(l, i, fn + (')' if '(' in fn else ''), prev_line,
                                  next_line, prev_prev_line, next_next_line, severity,
                                  verbose)
        else:
            for fn in pefdefs.exploitableFunctions:
                # there has to be space before function call; prevents from false-positives strings contains PHP function names
                atfn = "@{}".format(fn)
                fn = " {}".format(fn)
                # also, it has to checked agains @ at the beginning of the function name
                # @ prevents from output being echoed
                if fn in line or atfn in line:
                    header_printed = header_print(f.name, header_printed)
                    total += 1
                    printcodeline(l, i, fn + (')' if '(' in fn else ''), prev_line,
                                  next_line, prev_prev_line, next_next_line, severity,
                                  verbose)

        if critical == False:
            for dp in pefdefs.fileInclude:
                # there has to be space before function call; prevents from false-positives strings contains PHP function names
                dp = " {}".format(dp)
                # remove spaces to allow detection eg. include(  $_GET['something]  )
                if dp in line.replace(" ", ""):
                    header_printed = header_print(f.name, header_printed)
                    total += 1
                    printcodeline(l, i, dp + '()', prev_line, next_line,
                                  prev_prev_line, next_next_line, severity,
                                  verbose)

            for globalvars in pefdefs.globalVars:
                if globalvars in line:
                    header_printed = header_print(f.name, header_printed)
                    total += 1
                    printcodeline(l, i, globalvars, prev_line, next_line,
                                  prev_prev_line, next_next_line, severity,
                                  verbose)

            for refl in pefdefs.reflectedProperties:
                if refl in line:
                    header_printed = header_print(f.name, header_printed)
                    total += 1
                    printcodeline(l, i, refl, prev_line, next_line,
                                  prev_prev_line, next_next_line, severity,
                                  verbose)

            if sql == True:
                for refl in pefdefs.otherPatterns:
                    p = re.compile(refl)
                    if p.search(l):
                        header_printed = header_print(
                            f.name, header_printed)
                        total += 1
                        printcodeline(l, i, refl, prev_line, next_line,
                                      prev_prev_line, next_next_line, severity,
                                      verbose)

    if total < 1:
        pass
    else:
        print beautyConsole.getColor("red") + \
            "Found %d interesting entries\n" % (total) + \
            beautyConsole.getSpecialChar("endline")

    return total  # return how many findings in current file


# main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    filename = '.'  # initial value for file/dir to scan is current directory

    parser.add_argument(
        "-r", "--recursive", help="scan PHP files recursively in directory pointed by -f/--file", action="store_true")
    parser.add_argument(
        "-c", "--critical", help="look only for critical functions", action="store_true")
    parser.add_argument(
        "-s", "--sql", help="look for raw SQL queries", action="store_true")
    parser.add_argument(
        "-v", "--verbose", help="print verbose output (more code, docs)", action="store_true")
    parser.add_argument(
        "-n", "--noglobals", help="only functions (no $_XXX)", action="store_true")
    parser.add_argument(
        "-f", "--file", help="File or directory name to scan (if directory name is provided, make sure -r/--recursive is set)")
    args = parser.parse_args()

    verbose = True if args.verbose else False
    sql = True if args.sql else False
    critical = True if args.critical else False
    filename = args.file

    scanned_files = 0
    found_entries = 0

    severity = {
        "high": 0,
        "medium": 0,
        "low": 0
    }

    if args.recursive:
        for root, subdirs, files in os.walk(filename):
            for f in files:
                scanned_files = scanned_files + 1
                res = main(os.path.join(root, f), severity,
                           verbose, sql, critical)
                found_entries = found_entries + res
    else:
        scanned_files = scanned_files + 1
        found_entries = main(filename, severity)

    print beautyConsole.getColor("white") + "-" * 100

    print beautyConsole.getColor("green")
    print "\n>>>  {} file(s) scanned".format(scanned_files)
    if found_entries > 0:
        print "{}>>>  {} interesting entries found\n".format(
            beautyConsole.getColor("red"), found_entries)
    else:
        print "  No interesting entries found :( \n"

    print "{}==>  {}:\t {}".format(
        beautyConsole.getColor("red"), "HIGH", severity.get("high"))
    print "{}==>  {}:\t {}".format(beautyConsole.getColor(
        "yellow"), "MEDIUM", severity.get("medium"))
    print "{}==>  {}:\t {}".format(beautyConsole.getColor(
        "green"), "LOW", severity.get("low"))

    print "\n"

    # REFACTORED STARTS HERE
    engine = PefEngine(args.recursive, verbose, critical, sql, filename)

    exit(0)
