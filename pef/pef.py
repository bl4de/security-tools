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


def printcodeline(_line, i, _fn, _message, prev_line="", next_line="", prev_prev_line="", next_next_line="", __severity={}):
    """
    Formats and prints line of output
    """

    print "::  line %d ::   \33[33;1m%s\33[0m %s found " % (i, _fn, _message)
    if _fn and _fn.strip() in pefdocs.exploitableFunctionsDesc.keys():
        print "\n  " + beautyConsole.getColor("white") + pefdocs.exploitableFunctionsDesc.get(
            _fn.strip())[0] + beautyConsole.getSpecialChar("endline")
        print "  " + beautyConsole.getColor("grey") + pefdocs.exploitableFunctionsDesc.get(
            _fn.strip())[1] + beautyConsole.getSpecialChar("endline")
        print "  Potential impact: " + beautyConsole.getColor("red") + pefdocs.exploitableFunctionsDesc.get(
            _fn.strip())[2] + beautyConsole.getSpecialChar("endline")
        if pefdocs.exploitableFunctionsDesc.get(_fn.strip())[3] not in __severity.keys():
            __severity[pefdocs.exploitableFunctionsDesc.get(_fn.strip())[
                3]] = 1
        else:
            __severity[pefdocs.exploitableFunctionsDesc.get(_fn.strip(
            ))[3]] = __severity[pefdocs.exploitableFunctionsDesc.get(_fn.strip())[3]] + 1

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


def main(src, __severity):
    """
    performs code analysis, line by line
    """
    _file = open(src, "r")
    i = 0
    total = 0
    filenamelength = len(src)
    linelength = 97
    all_lines = _file.readlines()

    prev_prev_line = ""
    prev_line = ""
    next_line = ""
    next_next_line = ""

    print "FILE: \33[33m%s\33[0m " % os.path.realpath(_file.name), "\n"

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
        __line = _line.strip()
        for _fn in pefdefs.exploitableFunctions:
            # there has to be space before function call; prevents from false-positives strings contains PHP function names
            _fn = " {}".format(_fn)
            if _fn in __line:
                total += 1
                printcodeline(_line, i, _fn + (')' if '(' in _fn else ''),
                              beautyConsole.efMsgFound, prev_line, next_line, prev_prev_line, next_next_line, __severity)
        for _dp in pefdefs.fileInclude:
            # there has to be space before function call; prevents from false-positives strings contains PHP function names
            _dp = " {}".format(_dp)
            # remove spaces to allow detection eg. include(  $_GET['something]  )
            if _dp in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _dp + '()',
                              beautyConsole.fiMsgFound, prev_line, next_line, prev_prev_line, next_next_line, __severity)
        for _global in pefdefs.globalVars:
            if _global in __line:
                total += 1
                printcodeline(_line, i, _global,
                              beautyConsole.efMsgGlobalFound, prev_line, next_line, prev_prev_line, next_next_line, __severity)
        for _refl in pefdefs.reflectedProperties:
            if _refl in __line:
                total += 1
                printcodeline(_line, i, _refl,
                              beautyConsole.eReflFound, prev_line, next_line, prev_prev_line, next_next_line, __severity)

    if total < 1:
        print beautyConsole.getColor("green") + \
            "No exploitable functions found" + \
            beautyConsole.getSpecialChar("endline")
    else:
        print beautyConsole.getColor("red") + \
            "Found %d exploitable function(s)\n" % (total) + \
            beautyConsole.getSpecialChar("endline")

    print beautyConsole.getColor("white") + "-" * 100

    return total  # return how many findings in current file


# main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    __filename = '.'  # initial value for file/dir to scan is current directory

    parser.add_argument(
        "-r", "--recursive", help="scan PHP files recursively in current directory", action="store_true")
    parser.add_argument(
        "-f", "--file", help="File or directory name to scan (if directory name is provided, make sure -r/--recursive is set")
    args = parser.parse_args()

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
                res = main(os.path.join(root, f), __severity)
                __found_entries = __found_entries + res
    else:
        __scanned_files = __scanned_files + 1
        __found_entries = main(__filename, __severity)

    print beautyConsole.getColor("green")
    print "\n  {}file(s) scanned".format(__scanned_files)
    if __found_entries > 0:
        print "{}  {} interesting entries found\n".format(
            beautyConsole.getColor("red"), __found_entries)
    else:
        print "  No interesting entries found :( \n"

    print "    {}{}: {}".format(
        beautyConsole.getColor("red"), "HIGH", __severity.get("high"))
    print "    {}{}: {}".format(beautyConsole.getColor(
        "yellow"), "MEDIUM", __severity.get("medium"))
    print "    {}{}: {}".format(beautyConsole.getColor(
        "green"), "LOW", __severity.get("low"))

    print "\n"

    exit(0)
