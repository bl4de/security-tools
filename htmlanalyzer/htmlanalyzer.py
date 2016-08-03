#!/usr/bin/env python
#
# HTML source analyzer
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import argparse
import os

import modules.detection_engine
import modules.utils


# @TODO: Python doc in functions and for module
# @TODO: args parser for: -c (comments) -s (links/src), -j (JavaScript)


# find interesting string(s)
def analyze_line(_line, i):
    """single HTML source code analyze"""
    modules.detection_engine.detect_comments(_line, i)
    modules.detection_engine.detect_admin_stuff(_line, i)
    modules.detection_engine.detect_debug(_line, i)
    modules.detection_engine.detect_external_resources(_line, i)
    modules.detection_engine.detect_javascript(_line, i)


def main(_filename):
    """main program loop"""
    _ident = ""
    _fw = ""

    try:
        _file = open(_filename, "r")
        print "[+] {} opened, starting analysis...\n\n".format(_filename)
    except:
        msg = "[-] {} does not exists or could not be opened, quitting!" \
            .format(_filename)
        exit(msg)

    i = 0
    modules.utils.print_banner()

    for _line in _file:
        i += 1
        analyze_line(_line, i)
        if _ident == "":
            _ident = modules.detection_engine.identify(_line)
        if _fw == "":
            _fw = modules.detection_engine.detect_framework(_line)

    modules.utils.show_stats(_file, i, _ident, _fw)
    print (modules.utils.summary)


if __name__ == "__main__":
    """main program - run HTML analyze"""
    parser = argparse.ArgumentParser(description="HTML static code analyze")
    parser.add_argument('-u', help='Target url - index.html will be downloaded')
    parser.add_argument('-f', help='HTML file name to analyze')
    _filename = "index.html"
    args = parser.parse_args()

    if args.u:
        print "[+] connecting to {}...\n\n".format(args.u)
        os.system("curl --silent -o index.html " + args.u)
        print "[+] default index.html saved"
    if args.f and not args.u:
        _filename = args.f

    main(_filename)
