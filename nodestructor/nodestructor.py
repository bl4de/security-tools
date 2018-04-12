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
import argparse

from imports.beautyConsole import beautyConsole


BANNER = """
#####  nodestructor.py - static code analysis for Node.js applications  #####
# GitHub: bl4de | Twitter: @_bl4de | hackerone.com/bl4de | bloorq@gmail.com #

examples:   $ ./nodestructor filename.js
            $ ./nodestructor -R ./dirname
            $ ./nodestructor -R ./dirname --skip-node-modules --skip-test-files
            $ ./nodestructor -R ./node_modules --exclude babel,lodash,ansi
"""

PATTERNS = [
    ".*url.parse\(",
    ".*[pP]ath.normalize\(",
    ".*fs.*File.*\(",
    ".*fs.*Read.*\(",
    ".*process.cwd\(",
    ".*pipe\(res",
    ".*bodyParser\(",
    ".*eval\(",
    ".*res.write\(",
    ".*<a.*href.*>",
    ".*<img.*src.*>",
    ".*<iframe.*src.*>",
    ".*__dirname.*",
    ".*child_process.exec\(",
    ".* Function\(",
    ".*execFile\(",
    ".*spawn\(",
    ".*fork\(",
    # ".*replace\("
]

# for test purposes only :)
# PATTERNS = [
#     ".*[pP]ath.normalize\("
# ]

TOTAL_FILES = 0
PATTERNS_IDENTIFIED = 0
FILES_WITH_IDENTIFIED_PATTERNS = 0

# some files not to loking in:
EXTENSIONS_TO_IGNORE = ['md', 'txt', 'map', 'jpg', 'png']
MINIFIED_EXT = ['.min.js']
SKIP_ALWAYS = ['package.json', 'README.md']
TEST_FILES = ['test.js', 'tests.js']
SKIP_NODE_MODULES = False
SKIP_TEST_FILES = False
EXCLUDE = []
EXCLUDE_ALWAYS = ['babel', 'lodash', 'ansi', 'core-util', '.bin',
                  'core-js', 'es5', 'es6', 'convert-source-map', 'source-map-']


def show_banner():
    """
    Prints welcome banner with contact info
    """
    print beautyConsole.getColor("cyan")
    print BANNER
    print beautyConsole.getColor("white")


def printcodeline(_line, i, _fn, _message):
    _fn = _fn.replace("*", "").replace("\\", "").replace(".(", '(')[1:len(_fn)]
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
            if __rex.match(__line.replace(' ', '')):
                if print_filename:
                    FILES_WITH_IDENTIFIED_PATTERNS = FILES_WITH_IDENTIFIED_PATTERNS + 1
                    print "FILE: \33[33m{}\33[0m\n".format(src)
                    print_filename = False
                patterns_found_in_file += 1
                printcodeline(_line, i, __pattern,
                              ' code pattern identified: ')

    if patterns_found_in_file > 0:
        PATTERNS_IDENTIFIED = PATTERNS_IDENTIFIED + patterns_found_in_file
        print beautyConsole.getColor("red") + \
            "Identified %d code pattern(s)\n" % (patterns_found_in_file) + \
            beautyConsole.getSpecialChar("endline")
        print beautyConsole.getColor("white") + "-" * 100


# main program
if __name__ == "__main__":
    show_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Specify a file or directory to scan")
    parser.add_argument(
        "-R", "--recursive", help="check files recursively", action="store_true")
    parser.add_argument(
        "-E", "--exclude", help="comma separated list of packages to exclude from scanning (eg. babel excludes ALL packages with babel in name, like babel-register, babel-types etc.")
    parser.add_argument(
        "-S", "--skip-node-modules", help="when scanning recursively, do not scan ./node_modules folder", action="store_true")
    parser.add_argument(
        "-T", "--skip-test-files", help="when scanning recursively, do not check test files (usually test.js)", action="store_true")

    args = parser.parse_args()

    try:
        BASE_PATH = args.filename
        if args.recursive:
            FILE_LIST = os.listdir(args.filename)
        if args.exclude:
            EXCLUDE = [e for e in args.exclude.split(',')] + EXCLUDE_ALWAYS
        else:
            EXCLUDE = EXCLUDE_ALWAYS

        SKIP_NODE_MODULES = args.skip_node_modules
        SKIP_TEST_FILES = args.skip_test_files

        if args.recursive:
            for subdir, dirs, files in os.walk(BASE_PATH):

                if not True in [e in subdir for e in EXCLUDE]:
                    for __file in files:
                        FILENAME = os.path.join(subdir, __file)
                        if (FILENAME[-3:] not in EXTENSIONS_TO_IGNORE
                                and FILENAME not in SKIP_ALWAYS
                                and FILENAME[-2:] not in EXTENSIONS_TO_IGNORE
                                and FILENAME[-7:] not in MINIFIED_EXT):

                            if not '/node_modules/' in subdir or ('/node_modules/' in subdir and SKIP_NODE_MODULES is False):
                                if (SKIP_TEST_FILES is False):
                                    main(FILENAME)
                                    TOTAL_FILES = TOTAL_FILES + 1
                                else:
                                    if __file not in TEST_FILES and "/test" not in FILENAME and "/tests" not in FILENAME:
                                        main(FILENAME)
                                        TOTAL_FILES = TOTAL_FILES + 1
        else:
            FILENAME = args.filename
            if (FILENAME[-3:] not in EXTENSIONS_TO_IGNORE
                and FILENAME[-2:] not in EXTENSIONS_TO_IGNORE
                    and FILENAME[-7:] not in MINIFIED_EXT):
                main(FILENAME)
                TOTAL_FILES = TOTAL_FILES + 1

    except Exception as ex:
        print beautyConsole.getColor(
            "red"), "An exception occured: {}\n\n".format(ex)
        exit(1)

    print beautyConsole.getColor("cyan")
    print " {} file(s) scanned in total".format(TOTAL_FILES)
    if PATTERNS_IDENTIFIED > 0:
        print beautyConsole.getColor("red")
        print "Identified {} code pattern(s) in {} file(s)".format(
            PATTERNS_IDENTIFIED, FILES_WITH_IDENTIFIED_PATTERNS)
    else:
        print beautyConsole.getColor(
            "green"), "No code pattern identified"
    print beautyConsole.getColor("white")
