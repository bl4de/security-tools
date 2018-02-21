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
from __future__ import print_function
import sys
import os

from imports import pefdefs
from imports.beautyConsole import beautyConsole


def banner():
    """
    Prints welcome banner with contact info
    """
    print(beautyConsole.getColor("green") + "\n\n", "-" * 100)
    print("-" * 6, " PEF | PHP Exploitable Functions scanner", " " * 35, "-" * 16)
    print("-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ", " " * 22, "-" * 16)
    print("-" * 100, "\33[0m\n")


def printcodeline(_line, i, _fn, _message):
    """
    Formats and prints line of output
    """
    print("::  line %d :: \33[33;1m%s\33[0m %s found " % (i, _fn, _message))
    print(beautyConsole.getColor("grey") + _line + beautyConsole.getSpecialChar("endline"))


def main(src):
    """
    performs code analysis, line by line
    """
    _file = open(src, "r")
    i = 0
    total = 0
    filenamelength = len(src)
    linelength = 97

    print("-" * 14, " FILE: \33[33m%s\33[0m " % src, "-" * (linelength - filenamelength - 21), "\n")

    for _line in _file:
        i += 1
        __line = _line.strip()
        for _fn in pefdefs.exploitableFunctions:
            if _fn in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _fn + ')',
                              beautyConsole.efMsgFound)
        for _kw in pefdefs.keywords:
            if _kw.lower() in __line.lower():
                total += 1
                printcodeline(_line, i, _kw,
                              beautyConsole.eKeyWordFound)
        for _dp in pefdefs.fileInclude:
            if _dp in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _dp + '()',
                              beautyConsole.fiMsgFound)
        for _global in pefdefs.globalVars:
            if _global in __line:
                total += 1
                printcodeline(_line, i, _global,
                              beautyConsole.efMsgGlobalFound)
        for _refl in pefdefs.reflectedProperties:
            if _refl in __line:
                total += 1
                printcodeline(_line, i, _refl,
                              beautyConsole.eReflFound)

    if total < 1:
        print(beautyConsole.getColor("green") + \
            "No exploitable functions found\n" + \
            beautyConsole.getSpecialChar("endline"))
    else:
        print(beautyConsole.getColor("red") + \
            "Found %d exploitable functions total\n" % (total) + \
            beautyConsole.getSpecialChar("endline"))

    print(beautyConsole.getColor("white") + "-" * 100)


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

        print()
    else:
        print("Enter PHP or directory name with file(s) to analyse")
        print("single file: pef filename.php")
        print("directory: pef -R dirname")
