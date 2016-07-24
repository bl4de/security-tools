#!/usr/bin/env python
#
# HTML source analyzer
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import sys

from modules.console_output_beautifier import ConsoleOutputBeautifier


# TODO: Python doc in functions and for module
# TODO: args parser for: -c (comments) -s (links/src), -j (JavaScript)

def main():
    _ident = ""
    _fw = ""

    try:
        _file = open(sys.argv[1], "r")
    except:
        pass

    i = 0
    print_banner()

    for _line in _file:
        i += 1
        analyze_line(_line, i)
        if _ident == "":
            _ident = identify(_line)
        if _fw == "":
            _fw = detect_framework(_line)

    show_stats(_file, i, _ident, _fw)


# header
def print_banner():
    print ConsoleOutputBeautifier.getColor("green"), \
        "=" * 26, \
        "HTML source code Analyzer", "=" * 26, \
        "\n", \
        " " + "-" * 10, \
        "   https://github.com/bl4de | https://twitter.com/_bl4de " \
        "| bloorq@gmail.com   ", \
        "-" * 10, \
        "\n\n", \
        ConsoleOutputBeautifier.getSpecialChar("endline")


# detects frontend framework used
def detect_framework(_line):
    _fw = ""
    if "ng-app" in _line:
        _fw = "Angular 1.*"
    return _fw


# using osftare recognition
def identify(_line):
    _ident = "unknown"
    if "Jommla" in _line:
        _ident = "Joomla CMS"
    if "wp-content" in _line:
        _ident = "WordPress CMS"
    return _ident


def show_stats(_file, i, _ident, _fw):
    print ConsoleOutputBeautifier.getColor(
        "green"), "\n------ SUMMARY -------\n"
    print "total lines of code:     %d" % (i)
    print "identified CMS:          %s" % (_ident)
    print "identified framework:    %s" % (
        _fw), ConsoleOutputBeautifier.getSpecialChar("endline")
    # end of summary
    print "\n"


def print_output_line(i, col, msg, args):
    print ConsoleOutputBeautifier.getColor("white"), "line %d:" % (
        i), col, msg % (args), ConsoleOutputBeautifier.getSpecialChar("endline")


def detect_comments(_line, i):
    if '<!--' in _line.lstrip():
        if "\"/" in _line:
            print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                              "COMMENTED PATH found at line %d:   %s",
                              (i, _line.lstrip().rstrip()))
        else:
            print_output_line(i, ConsoleOutputBeautifier.getColor("yellow"),
                              "COMMENT found at line %d:   %s",
                              (i, _line.lstrip().rstrip()))


def detect_admin_stuff(_line, i):
    if "admin" in _line.lower():
        print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                          "'admin' string found at line: %d", i)


def detect_debug(_line, i):
    if "debug" in _line.lower():
        print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                          "DEBUG information found at line %d", i)


def detect_external_resources(_line, i):
    if "src" in _line.lower():
        if "<img" in _line.lower():
            print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                              "PATH to external resource image "
                              " file found in %d:   %s",
                              (i, _line.lstrip().rstrip()[0:80]))
        if "<iframe" in _line.lower():
            print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                              "IFRAME path found in %d:   %s",
                              (i, _line.lstrip().rstrip()[0:80]))
        if "<script" in _line.lower():
            print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                              "external SCRIPT path found in %d:   %s",
                              (i, _line.lstrip().rstrip()[0:80]))


def detect_javascript(_line, i):
    if "<script" in _line.lower() and "src" not in _line.lower():
        print_output_line(i, ConsoleOutputBeautifier.getColor("green"),
                          "inline <SCRIPT> tag found at line %d", i)
    if "javascript:" in _line.lower():
        print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                          "INLINE JavaScript event handler found at line %d", i)


# find interesting string(s)
def analyze_line(_line, i):
    detect_comments(_line, i)
    detect_admin_stuff(_line, i)
    detect_debug(_line, i)
    detect_external_resources(_line, i)
    detect_javascript(_line, i)


# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print "Enter HTML file name"
