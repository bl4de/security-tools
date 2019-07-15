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

    def __init__(self):
        """
        constructor
        """
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


def printcodeline(_line, i, _fn, prev_line="", next_line="", prev_prev_line="", next_next_line="", __severity={}, __verbose=False):
    """
    Formats and prints line of output
    """
    __impact_color = {
        "low": "green",
        "medium": "yellow",
        "high": "red"
    }

    if __verbose == True:
        print " line %d :: \33[33;1m%s\33[0m " % (i, _fn)
    else:
        print "{}line {} :: {}{} ".format(beautyConsole.getColor(
            "white"), i, beautyConsole.getColor("grey"), _line.strip())

    # print legend only if there i sentry in pefdocs.py
    if _fn and _fn.strip() in pefdocs.exploitableFunctionsDesc.keys():
        __impact = pefdocs.exploitableFunctionsDesc.get(_fn.strip())[3]
        __description = pefdocs.exploitableFunctionsDesc.get(_fn.strip())[
            0]
        __syntax = pefdocs.exploitableFunctionsDesc.get(_fn.strip())[1]
        __vuln_class = pefdocs.exploitableFunctionsDesc.get(_fn.strip())[2]

        if __verbose == True:
            print "\n  {}{}{}".format(beautyConsole.getColor(
                "white"), __description, beautyConsole.getSpecialChar("endline"))
            print "  {}{}{}".format(beautyConsole.getColor(
                "grey"), __syntax, beautyConsole.getSpecialChar("endline"))
            print "  Potential impact: {}{}{}".format(beautyConsole.getColor(
                __impact_color[__impact]), __vuln_class, beautyConsole.getSpecialChar("endline"))

        if __impact not in __severity.keys():
            __severity[__impact] = 1
        else:
            __severity[__impact] = __severity[__impact] + 1

    if __verbose == True:
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


def main(src, __severity, __verbose=False, __sql=False, __critical=False):
    """
    performs code analysis, line by line
    """
    _file = open(src, "r")
    i = 0
    total = 0
    filenamelength = len(src)
    linelength = 97
    all_lines = _file.readlines()

    header_printed = False
    prev_prev_line = ""
    prev_line = ""
    next_line = ""
    next_next_line = ""

    for _line in all_lines:
        if i > 2:
            prev_prev_line = all_lines[i - 2].rstrip()
        if i > 1:
            prev_line = all_lines[i - 1].rstrip()
        if i < (len(all_lines) - 1):
            next_line = all_lines[i + 1].rstrip()
        if i < (len(all_lines) - 2):
            next_next_line = all_lines[i + 2].rstrip()

        i += 1
        __line = _line.rstrip()

        if __critical:
            for _fn in pefdefs.critical:
                # there has to be space before function call; prevents from false-positives strings contains PHP function names
                _at_fn = "@{}".format(_fn)
                _fn = " {}".format(_fn)
                # also, it has to checked agains @ at the beginning of the function name
                # @ prevents from output being echoed
                if _fn in __line or _at_fn in __line:
                    header_printed = header_print(_file.name, header_printed)
                    total += 1
                    printcodeline(_line, i, _fn + (')' if '(' in _fn else ''), prev_line,
                                  next_line, prev_prev_line, next_next_line, __severity, __verbose)
        else:
            for _fn in pefdefs.exploitableFunctions:
                # there has to be space before function call; prevents from false-positives strings contains PHP function names
                _at_fn = "@{}".format(_fn)
                _fn = " {}".format(_fn)
                # also, it has to checked agains @ at the beginning of the function name
                # @ prevents from output being echoed
                if _fn in __line or _at_fn in __line:
                    header_printed = header_print(_file.name, header_printed)
                    total += 1
                    printcodeline(_line, i, _fn + (')' if '(' in _fn else ''), prev_line,
                                  next_line, prev_prev_line, next_next_line, __severity, __verbose)

        if __critical == False:
            for _dp in pefdefs.fileInclude:
                # there has to be space before function call; prevents from false-positives strings contains PHP function names
                _dp = " {}".format(_dp)
                # remove spaces to allow detection eg. include(  $_GET['something]  )
                if _dp in __line.replace(" ", ""):
                    header_printed = header_print(_file.name, header_printed)
                    total += 1
                    printcodeline(_line, i, _dp + '()', prev_line, next_line,
                                  prev_prev_line, next_next_line, __severity, __verbose)

            for _global in pefdefs.globalVars:
                if _global in __line:
                    header_printed = header_print(_file.name, header_printed)
                    total += 1
                    printcodeline(_line, i, _global, prev_line, next_line,
                                  prev_prev_line, next_next_line, __severity, __verbose)

            for _refl in pefdefs.reflectedProperties:
                if _refl in __line:
                    header_printed = header_print(_file.name, header_printed)
                    total += 1
                    printcodeline(_line, i, _refl, prev_line, next_line,
                                  prev_prev_line, next_next_line, __severity, __verbose)

            if __sql == True:
                for _refl in pefdefs.otherPatterns:
                    p = re.compile(_refl)
                    if p.search(_line):
                        header_printed = header_print(
                            _file.name, header_printed)
                        total += 1
                        printcodeline(_line, i, _refl, prev_line, next_line,
                                      prev_prev_line, next_next_line, __severity, __verbose)

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
    __filename = '.'  # initial value for file/dir to scan is current directory

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

    __verbose = True if args.verbose else False
    __sql = True if args.sql else False
    __critical = True if args.critical else False
    __filename = args.file

    __scanned_files = 0
    __found_entries = 0

    __severity = {
        "high": 0,
        "medium": 0,
        "low": 0
    }

    if args.recursive:
        for root, subdirs, files in os.walk(__filename):
            for f in files:
                __scanned_files = __scanned_files + 1
                res = main(os.path.join(root, f), __severity,
                           __verbose, __sql, __critical)
                __found_entries = __found_entries + res
    else:
        __scanned_files = __scanned_files + 1
        __found_entries = main(__filename, __severity)

    print beautyConsole.getColor("white") + "-" * 100

    print beautyConsole.getColor("green")
    print "\n>>>  {} file(s) scanned".format(__scanned_files)
    if __found_entries > 0:
        print "{}>>>  {} interesting entries found\n".format(
            beautyConsole.getColor("red"), __found_entries)
    else:
        print "  No interesting entries found :( \n"

    print "{}==>  {}:\t {}".format(
        beautyConsole.getColor("red"), "HIGH", __severity.get("high"))
    print "{}==>  {}:\t {}".format(beautyConsole.getColor(
        "yellow"), "MEDIUM", __severity.get("medium"))
    print "{}==>  {}:\t {}".format(beautyConsole.getColor(
        "green"), "LOW", __severity.get("low"))

    print "\n"

    exit(0)
