#!/usr/bin/python
#
# HTML source analyzer
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import sys


class PefOutput:
    Black = '\33[30m'
    Red = '\33[31m'
    Green = '\33[32m'
    Yellow = '\33[33m'
    Blue = '\33[34m'
    Magenta = '\33[35m'
    Cyan = '\33[36m'
    White = '\33[37m'
    _endline = '\33[0m'

    efMsgFound = "exploitable function call"
    efMsgGlobalFound = "global variable explicit call"


_ident = "unknown"


def main():
    _file = open(sys.argv[1], "r")
    i = 0
    print PefOutput.Green, "=" * 26, "HTML source code Analyzer", "=" * 26
    print "-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ", "-" * 6, PefOutput._endline

    print
    for _line in _file:
        i += 1
        analyze_line(_line, i)
        identify(_line)
    show_stats(_file, i)


# using osftare recognition
def identify(_line):
    if "Jommla" in _line:
        _ident = "Joomla CMS"
    if "wp-content" in _line:
        _ident = "WordPress CMS"


def show_stats(_file, i):
    print PefOutput.Green, "\n------ SUMMARY -------\n"
    print "total lines of code: %d" % (i)
    print "identified software: %s" % (_ident), PefOutput._endline
    # end of summary
    print "\n"


# find interesting string(s)
def analyze_line(_line, i):
    if _line.lstrip().startswith('<!--'):
        print PefOutput.White, "line %d:" % (
            i), PefOutput.Yellow, "comment found at line %d: %s" % (
            i, _line.rstrip()), PefOutput._endline
    if "admin" in _line:
        print PefOutput.White, "line %d:" % (
            i), PefOutput.Red, "'admin' string found at line: %d" % (
            i), PefOutput._endline
    if "debug" in _line:
        print PefOutput.White, "line %d:" % (
            i), PefOutput.Red, "debug information found at line %d" % (
            i), PefOutput._endline
    if "src=" in _line:
        print PefOutput.White, "line %d:" % (
            i), PefOutput.Cyan, "path to file found in %d" % (
            i), PefOutput._endline
    if "<script>" in _line:
        print PefOutput.White, "line %d:" % (
            i), PefOutput.Cyan, "script tag found at line %d" % (
            i), PefOutput._endline
    if "javascript:" in _line:
        print PefOutput.White, "line %d:" % (
            i), PefOutput.Cyan, "inline JavaScript found at line %d" % (
            i), PefOutput._endline
    if "\"/" in _line:
        print PefOutput.White, "line %d:" % (
            i), PefOutput.Magenta, "possible directory path found at line %d" % (
            i), PefOutput._endline


# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print "Enter HTML file name"
