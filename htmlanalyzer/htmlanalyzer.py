#!/usr/bin/env python
#
# HTML source analyzer
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import sys


# TODO: Python doc in functions and for module
# TODO: args parser for: -c (comments) -s (links/src), -j (JavaScript)

class ConsoleOutputBeautifier:
    """This class defines properties and methods to manipulate console output"""
    colors = {
        "black": '\33[30m',
        "white": '\33[37m',
        "red": '\33[31m',
        "green": '\33[32m',
        "yellow": '\33[33m',
        "blue": '\33[34m',
        "magenta": '\33[35m',
        "cyan": '\33[36m'
    }

    characters = {
        "endline": '\33[0m'
    }

    def __init__(self):
        return None

    def getColor(self, color_name):
        """returns color identified by color_name or white as default value"""
        if color_name in ConsoleOutputBeautifier.colors:
            return ConsoleOutputBeautifier.colors[color_name]
        return ConsoleOutputBeautifier.colors["white"]

    def getSpecialChar(self, char_name):
        """returns special character identified by char_name"""
        if char_name in ConsoleOutputBeautifier.characters:
            return ConsoleOutputBeautifier.characters[char_name]
        return ""


co = ConsoleOutputBeautifier()


def main():
    _ident = ""
    _fw = ""

    try:
        _file = open(sys.argv[1], "r")
    except:
        pass

    i = 0
    print_header()

    for _line in _file:
        i += 1
        analyze_line(_line, i)
        if _ident == "":
            _ident = identify(_line)
        if _fw == "":
            _fw = detect_framework(_line)

    show_stats(_file, i, _ident, _fw)


# header
def print_header():
    print co.getColor("green"), "=" * 26, "HTML source code Analyzer", "=" * 26
    print " " + "-" * 10, "   https://github.com/bl4de | https://twitter.com/_bl4de | bloorq@gmail.com   ", \
        "-" * 10, "\n\n", co.getSpecialChar("endline")


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
    print co.getColor("green"), "\n------ SUMMARY -------\n"
    print "total lines of code:     %d" % (i)
    print "identified CMS:          %s" % (_ident)
    print "identified framework:    %s" % (
        _fw), co.getSpecialChar("endline")
    # end of summary
    print "\n"


def print_output_line(i, col, msg, args):
    print co.getColor("white"), "line %d:" % (
        i), col, msg % (args), co.getSpecialChar("endline")


# find interesting string(s)
def analyze_line(_line, i):
    if _line.lstrip().startswith('<!--'):
        if "\"/" in _line:
            print_output_line(i, co.getColor("red"),
                              "COMMENTED PATH found at line %d:   %s",
                              (i, _line.lstrip().rstrip()))
        else:
            print_output_line(i, co.getColor("yellow"),
                              "COMMENT found at line %d:   %s",
                              (i, _line.lstrip().rstrip()))
    if "admin" in _line:
        print_output_line(i, co.getColor("red"),
                          "'admin' string found at line: %d", i)
    if "debug" in _line:
        print_output_line(i, co.getColor("red"),
                          "debug information found at line %d", i)
    if "src=" in _line:
        print_output_line(i, co.getColor("cyan"),
                          "PATH to external resource file (IMG, CSS, JS)"
                          " file found in %d:   %s",
                          (i, _line.lstrip().rstrip()[0:80]))
    if "<script>" in _line:
        print_output_line(i, co.getColor("green"),
                          "<SCRIPT> tag found at line %d", i)
    if "javascript:" in _line:
        print_output_line(i, co.getColor("cyan"),
                          "INLINE JavaScript found at line %d", i)


# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print "Enter HTML file name"
