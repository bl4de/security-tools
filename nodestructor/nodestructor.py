#!/usr/bin/python
#
# nodestructor
# Node.js application static code analysis tool
#
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
"""
nodestructor.py - static code analysis for Node.js applications
by bl4de
GitHub: bl4de | Twitter: @_bl4de | hackerone.com/bl4de  bloorq@gmail.com
"""
import sys
import os

from imports.beautyConsole import beautyConsole


BANNER = """
nodestructor.py - static code analysis for Node.js applications
by bl4de
GitHub: bl4de | Twitter: @_bl4de | hackerone.com/bl4de | bloorq@gmail.com 
"""

PATTERNS = [
    ".readFile(",
    ".readFileSync(",
    ".resolve(",
    ".exec(",
    "setInterval(",
    "setTimeout(",
    "new Function(",
    "path.join("
]


def show_banner():
    """
    Prints welcome banner with contact info
    """
    print BANNER


def printcodeline(_line, i, _fn, _message):
    """
    Formats and prints line of output
    """
    print "::  line %d :: \33[33;1m%s\33[0m %s found " % (i, _fn, _message)
    print beautyConsole.getColor("grey") + _line + beautyConsole.getSpecialChar("endline")


def main(src):
    """
    performs code analysis, line by line
    """
    _file = open(src, "r")
    i = 0
    total = 0
    filenamelength = len(src)
    linelength = 97

    print "-" * 14, " FILE: \33[33m%s\33[0m " % src, "-" * (linelength - filenamelength - 21), "\n"

    for _line in _file:
        i += 1
        __line = _line.strip()
        for _fn in PATTERNS:
            if _fn in __line.replace(" ", ""):
                total += 1
                printcodeline(_line, i, _fn + ')',
                              beautyConsole.efMsgFound)

    if total < 1:
        print beautyConsole.getColor("green") + \
            "No dangerous functions found\n" + \
            beautyConsole.getSpecialChar("endline")
    else:
        print beautyConsole.getColor("red") + \
            "Found %d dangerous functions total\n" % (total) + \
            beautyConsole.getSpecialChar("endline")

    print beautyConsole.getColor("white") + "-" * 100


# main program
if __name__ == "__main__":

    if len(sys.argv) >= 2:
        show_banner()

        # main program loop
        if len(sys.argv) == 3 and (sys.argv[1] == "-R" or sys.argv[2] == "-R"):
            if sys.argv[1] == "-R":
                BASE_PATH = sys.argv[2] + '/'
                FILE_LIST = os.listdir(sys.argv[2])
            if sys.argv[2] == "-R":
                FILE_LIST = os.listdir(sys.argv[1])
                BASE_PATH = sys.argv[1] + '/'

            for __file in FILE_LIST:
                if __file[-3:] == ".js":
                    full_path = BASE_PATH + __file
                    if os.path.isfile(full_path):
                        main(full_path)
        else:
            main(sys.argv[1])

        print
    else:
        print "Enter JavaScript file name or directory name with file(s) to analyse"
        print "single file: ./nodestructor.py filename.js"
        print "directory: ./nodestructor.py -R dirname"
