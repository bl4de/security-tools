#!/usr/bin/env python

"""HTML source analyzer
    bl4de | bloorq@gmail.com | Twitter: @_bl4de | H1: bl4de

    This tool goes through HTML document and shows all interesting places,
    like inline JavaScript calls, commented paths, 'debug' and similar
    words occurences, possible DOM Injection points, references to 
    resources like images or iframes
"""

import argparse
import os

import modules.detection_engine
import modules.utils

from modules.console_output_beautifier import ConsoleOutputBeautifier


# @TODO: Python doc in functions and for module
# @TODO: args parser for: -c (comments) -s (links/src), -j (JavaScript)

# find interesting string(s)
def analyze_line(_line, i, include_comments, be_verbose):
    """single HTML source line - code analyze"""
    if include_comments == True:
        modules.detection_engine.detect_comments(_line, i)

    # shows only when -v is set
    if be_verbose == True:
        modules.detection_engine.detect_external_resources(_line, i)
        modules.detection_engine.detect_javascript(_line, i)

    modules.detection_engine.detect_admin_stuff(_line, i)
    modules.detection_engine.detect_debug(_line, i)
    modules.detection_engine.detect_dombased_xss(_line, i)
    modules.detection_engine.detect_developer_comments(_line, i)


def main(_filename, args):
    """main program loop"""
    _ident = ""
    _fw = ""

    # include comments?
    include_comments = True if args.c else False

    # be verbose?
    be_verbose = True if args.v else False

    try:
        _file = open(_filename, "r")
        print "[+] {} opened, starting analysis...\n\n".format(_filename)
    except:
        msg = "[-] {} does not exists or could not be opened, quitting!" \
            .format(_filename)
        exit(msg)

    i = 0

    print ConsoleOutputBeautifier.getColor(
        "green"), "\n------ ANALYSIS ------\n"

    for _line in _file:
        i += 1
        analyze_line(_line, i, include_comments, be_verbose)
        if _ident == "":
            _ident = modules.detection_engine.identify(_line)
        if _fw == "":
            _fw = modules.detection_engine.detect_framework(_line)

    modules.utils.show_stats(_file, i, _ident, _fw)
    # print (modules.utils.summary)


if __name__ == "__main__":
    """main program - run HTML analyze"""
    parser = argparse.ArgumentParser(description="HTML static code analyze")
    parser.add_argument(
        '-u', help='Target url - index.html will be downloaded')
    parser.add_argument('-f', help='HTML file name to analyze')
    parser.add_argument(
        '-c', help='include comments in summary (excluded by default)')
    parser.add_argument(
        '-v', help='verbose; shows all messages (default - shows only '
        'critical, like possible injection points or debug info occurence)'
    )

    # let's go
    modules.utils.print_banner()

    _filename = "index.html"
    args = parser.parse_args()

    if args.u:
        print "[+] connecting to {}...".format(args.u)
        os.system(
            "curl -A 'htmlanalyzer' --header 'Host: {}'--silent -o index.html {}".format(args.u, args.u))
        print "[+] default index.html saved"
    if args.f and not args.u:
        _filename = args.f

    if not args.f and not args.u:
        print "[-] no filename (-f FILENAME) or url (-u URL); aborting!"
        exit(0)

    main(_filename, args)
