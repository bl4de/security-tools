#!/usr/bin/env python

"""HTML source analyzer
    bl4de | bloorq@gmail.com | Twitter: @_bl4de | H1: bl4de

    This tool goes through HTML document and shows all interesting places,
    like inline JavaScript calls, commented paths, 'debug' and similar
    words occurences, possible DOM Injection points, references to
    resources like images or iframes
"""
from __future__ import print_function
from __future__ import absolute_import
# @TODO: args PARSER for: -c (comments) -s (links/src), -j (JavaScript)
# @TODO: remove doubled line(s) - https://github.com/bl4de/security-tools/issues/15


import argparse
import os

from . import modules

from .modules.console_output_beautifier import ConsoleOutputBeautifier


# find interesting string(s)


def analyze_line(_line, i, include_comments, be_verbose):
    """single HTML source line - code analyze"""
    if include_comments is True:
        modules.detection_engine.detect_comments(_line, i)

    # shows only when -v is set
    if be_verbose is True:
        modules.detection_engine.detect_external_resources(_line, i)
        modules.detection_engine.detect_javascript(_line, i)
        modules.detection_engine.detect_developer_comments(_line, i)

    modules.detection_engine.detect_admin_stuff(_line, i)
    modules.detection_engine.detect_debug(_line, i)
    modules.detection_engine.detect_dombased_xss(_line, i)
    modules.detection_engine.detect_ajax_calls(_line, i)


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
        print("[+] {} opened, starting analysis...\n\n".format(_filename))
    except IOError:
        msg = "[-] {} does not exists or could not be opened, quitting!" \
            .format(_filename)
        exit(msg)

    i = 0

    print(ConsoleOutputBeautifier.getColor(
        "green"), "\n------ ANALYSIS ------\n")

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
    """
    main program - run HTML analyze
    """
    PARSER = argparse.ArgumentParser(description="HTML static code analyze")
    PARSER.add_argument(
        '-u', help='Target url - index.html will be downloaded')
    PARSER.add_argument(
        '-H', help='Target host - "Host" HTTP request header value')
    PARSER.add_argument('-f', help='HTML file name to analyze')
    PARSER.add_argument(
        '-c', help='include comments in summary (excluded by default)')
    PARSER.add_argument(
        '-v', help='verbose; shows all messages (default - shows only '
        'critical, like possible injection points or debug info occurence)'
    )

    # let's go
    modules.utils.print_banner()

    FILENAME = "index.html"
    ARGS = PARSER.parse_args()

    if ARGS.H and ARGS.u:
        print("[+] connecting to {}...".format(ARGS.u))
        os.system("curl -A 'htmlanalyzer' --header " +
                  "'Host: {}' --silent -o index.html {}".format(ARGS.H, ARGS.u))
        print("[+] default index.html saved")
    if ARGS.f and not ARGS.u:
        FILENAME = ARGS.f

    if not ARGS.f and not ARGS.u:
        print("[-] no filename (-f FILENAME) or url (-u URL); aborting!")
        exit(0)

    main(FILENAME, ARGS)
