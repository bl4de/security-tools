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

from imports import pefdefs
from imports.beautyConsole import beautyConsole


def banner():
    """
    Prints welcome banner with contact info
    """
    print beautyConsole.getColor("green") + "\n\n", "-" * 100
    print "-" * 6, " PEF | PHP Exploitable Functions scanner", " " * 35, "-" * 16
    print "-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ", " " * 22, "-" * 16
    print "-" * 100, "\33[0m\n"


def printcodeline(_line, i, _fn, _message, prev_line="", next_line="", prev_prev_line="", next_next_line=""):
    """
    Formats and prints line of output
    """
    print "::  line %d ::   \33[33;1m%s\33[0m %s found " % (i, _fn, _message)
    if _fn and pefdefs.exploitableFunctionsDesc.has_key(_fn):
        print "\t\t" + beautyConsole.getColor("white") + pefdefs.exploitableFunctionsDesc.get(
            _fn) + beautyConsole.getSpecialChar("endline")

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


def main(src):
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
            if _fn in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _fn + ')',
                              beautyConsole.efMsgFound, prev_line, next_line, prev_prev_line, next_next_line)
        for _dp in pefdefs.fileInclude:
            if _dp in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _dp + '()',
                              beautyConsole.fiMsgFound, prev_line, next_line, prev_prev_line, next_next_line)
        for _global in pefdefs.globalVars:
            if _global in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _global,
                              beautyConsole.efMsgGlobalFound, prev_line, next_line, prev_prev_line, next_next_line)
        for _refl in pefdefs.reflectedProperties:
            if _refl in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _refl,
                              beautyConsole.eReflFound, prev_line, next_line, prev_prev_line, next_next_line)

    if total < 1:
        print beautyConsole.getColor("green") + \
            "No exploitable functions found" + \
            beautyConsole.getSpecialChar("endline")
    else:
        print beautyConsole.getColor("red") + \
            "Found %d exploitable function(s)\n" % (total) + \
            beautyConsole.getSpecialChar("endline")

    print beautyConsole.getColor("white") + "-" * 100


# main program
if __name__ == "__main__":

    if len(sys.argv) >= 2:
        banner()

        # main program loop
        if len(sys.argv) == 3 and (sys.argv[1] == "-R" or sys.argv[2] == "-R"):
            if sys.argv[1] == "-R":
                base_path = sys.argv[2] + '/'
                file_list = os.listdir(sys.argv[2])
            if sys.argv[2] == "-R":
                file_list = os.listdir(sys.argv[1])
                base_path = sys.argv[1] + '/'

            for __file in file_list:
                full_path = base_path + __file
                if os.path.isfile(full_path):
                    main(full_path)
        else:
            main(sys.argv[1])

        print
    else:
        print "Enter PHP or directory name with file(s) to analyse"
        print "single file: pef filename.php"
        print "directory: pef -R dirname"
