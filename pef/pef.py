#!/usr/bin/python
#
# PHP Exploitable Functions/Vars Scanner
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import sys
import os

from imports import pefdefs
from imports.cco import ConsoleOutputBeautifier


# prints formated output line
def printcodeline(_line, i, _fn, _message):
    print "::  line %d :: \33[33;1m%s\33[0m %s found " % (i, _fn, _message)
    print ConsoleOutputBeautifier.getColor("blue") + _line + ConsoleOutputBeautifier.getSpecialChar("endline")


# performs code analysis, line by line
def main(srcfile):
    # open file to analyse
    _file = open(srcfile, "r")
    i = 0
    total = 0
    filenamelength = len(srcfile)
    linelength = 97

    print "-" * 14, " FILE: \33[33m%s\33[0m " % srcfile, "-" * (linelength - filenamelength - 21), "\n"

    for _line in _file:
        i += 1
        __line = _line.replace(" ", "")
        for _fn in pefdefs.exploitableFunctions:
            if _fn + '(' in __line or _fn + ' (' in __line:
                total += 1
                printcodeline(_line, i, _fn + '()',
                              ConsoleOutputBeautifier.efMsgFound)
        for _dp in pefdefs.fileInclude:
            if _dp in __line:
                total += 1
                printcodeline(_line, i, _dp + '()',
                              ConsoleOutputBeautifier.fiMsgFound)
        for _global in pefdefs.globalVars:
            if _global in __line:
                total += 1
                printcodeline(_line, i, _global,
                              ConsoleOutputBeautifier.efMsgGlobalFound)

    if total < 1:
        print ConsoleOutputBeautifier.getColor("green") + "No exploitable functions found\n" + ConsoleOutputBeautifier.getSpecialChar("endline")
    else:
        print ConsoleOutputBeautifier.getColor("red") + "Found %d exploitable functions total\n" % (total) + ConsoleOutputBeautifier.getSpecialChar("endline")

    print ConsoleOutputBeautifier.getColor("white") + "-" * 100


# main program
if __name__ == "__main__":

    if len(sys.argv) >= 2:
        print ConsoleOutputBeautifier.getColor("green") + "\n\n", "-" * 100
        print "-" * 6, " PEF | PHP Exploitable Functions scanner", " " * 35, "-" * 16
        print "-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ", " " * 22, "-" * 16
        print "-" * 100, "\33[0m\n"

        # main program loop
        if len(sys.argv) == 3 and sys.argv[1] == "-R":
            file_list = os.listdir(sys.argv[2])
            for __file in file_list:
                if os.path.isfile(__file) and '.php' in __file:
                    main(__file)
        else:
            main(sys.argv[1])

        print
    else:
        print "Enter PHP or directory name with file(s) to analyse"
        print "single file: pef filename.php"
        print "directory: pef -R dirname"
