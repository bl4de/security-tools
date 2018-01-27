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
import re

from imports.beautyConsole import beautyConsole


BANNER = """
#####  nodestructor.py - static code analysis for Node.js applications  #####
# GitHub: bl4de | Twitter: @_bl4de | hackerone.com/bl4de | bloorq@gmail.com #
"""

PATTERNS = [
    ".*url\.parse\(",
    ".*normalize\(",
    ".*fs.readFileSync\(",
    ".*f.readFile\(",
    ".*bodyParser()",
    ".*handlebars.SafeString\(",
    ".*eval\("
]

TOTAL_FILES = 0
PATTERNS_IDENTIFIED = 0
FILES_WITH_IDENTIFIED_PATTERNS = 0


def show_banner():
    """
    Prints welcome banner with contact info
    """
    print beautyConsole.getColor("cyan")
    print BANNER
    print beautyConsole.getColor("white")


def printcodeline(_line, i, _fn, _message):
    """
    Formats and prints line of output
    """
    print "::  line %d :: \33[33;1m%s\33[0m %s " % (i, _fn, _message)
    print beautyConsole.getColor("grey") + _line + \
        beautyConsole.getSpecialChar("endline")


def main(src):
    """
    performs code analysis, line by line
    """
    global PATTERNS_IDENTIFIED
    global FILES_WITH_IDENTIFIED_PATTERNS
    print_filename = True

    _file = open(src, "r")
    i = 0
    patterns_found_in_file = 0

    for _line in _file:
        i += 1
        __line = _line.strip()
        for __pattern in PATTERNS:
            __rex = re.compile(__pattern)
            if __rex.match(__line):
                if print_filename:
                    FILES_WITH_IDENTIFIED_PATTERNS = FILES_WITH_IDENTIFIED_PATTERNS + 1
                    print "FILE: \33[33m{}\33[0m\n".format(src)
                    print_filename = False
                patterns_found_in_file += 1
                printcodeline(_line, i, __pattern + ')',
                              ' dangerous pattern identified: ')

    if patterns_found_in_file > 0:
        PATTERNS_IDENTIFIED = PATTERNS_IDENTIFIED + patterns_found_in_file
        print beautyConsole.getColor("red") + \
            "Identified %d code pattern(s)\n" % (patterns_found_in_file) + \
            beautyConsole.getSpecialChar("endline")
        print beautyConsole.getColor("white") + "-" * 100


# main program
if __name__ == "__main__":

    if len(sys.argv) >= 2:
        show_banner()

        # main program loop
        if len(sys.argv) == 3 and (sys.argv[1] == "-R" or sys.argv[2] == "-R"):
            if sys.argv[1] == "-R":
                BASE_PATH = sys.argv[2]
                FILE_LIST = os.listdir(sys.argv[2])
            if sys.argv[2] == "-R":
                FILE_LIST = os.listdir(sys.argv[1])
                BASE_PATH = sys.argv[1]

            # build_file_list(BASE_PATH)

            for subdir, dirs, files in os.walk(BASE_PATH):
                for __file in files:
                    if __file[-3:] == ".js":
                        main(os.path.join(subdir, __file))
                        TOTAL_FILES = TOTAL_FILES + 1
        else:
            main(sys.argv[1])

        print

        # TODO summary by patter
        print beautyConsole.getColor("cyan")
        print " {} file(s) scanned in total".format(TOTAL_FILES)
        if PATTERNS_IDENTIFIED > 0:
            print beautyConsole.getColor(
                "red"), "Identified {} code pattern(s) in {} file(s)".format(PATTERNS_IDENTIFIED, FILES_WITH_IDENTIFIED_PATTERNS)
        else:
            print beautyConsole.getColor(
                "green"), "No code pattern identified"
        print beautyConsole.getColor("white")

    else:
        print "Enter JavaScript file name or directory name with file(s) to analyse"
        print "single file: ./nodestructor.py filename.js"
        print "directory: ./nodestructor.py -R dirname"
