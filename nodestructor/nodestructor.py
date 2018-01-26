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
    ".*eval\(",
    ".*(eval\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(setTimeout\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(setInterval\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(new Function\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(deserialize\(|unserialize\()",
    ".*(require\('js-yaml'\)\.load\(|yaml\.load\()",
    ".*(\[)*('|\")*NODE_TLS_REJECT_UNAUTHORIZED('|\")*(\])*(\s)*=(\s)*('|\")*0('|\")*",
    ".*noEscape(\s)*:(\s)*true",
    ".*SSL_VERIFYPEER(\s)*:(\s)*0",
    ".*createHash\(('|\")md5('|\")",
    ".*createHash\(('|\")sha1('|\")",
    ".*password\s*=\s*['|\"].+['|\"]\s{0,5}[;|.]",
    ".*\s*['|\"]password['|\"]\s*:",
    ".*\s*['|\"]+secret['|\"]+\s*:|\s*secret\s*:\s*['|\"]+",
    ".*username\s*=\s*['|\"].+['|\"]\s{0,5}[;|.]",
    ".*lusca.xssProtection\(false\)|X-XSS-Protection('|\")*(\s)*(:|,)(\s)*('|\")*0",
    ".*(\.createReadStream\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(\.readFile\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(res\.redirect\()( *)(req\.|req\.query|req\.body|req\.param)",
    ".*(SELECT|INSERT|UPDATE|DELETE|CREATE|EXPLAIN)(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(\.)(find|drop|create|explain|delete|count|bulk|copy)(.{0,4000})({(.{0,4000})\$where:)(.{0,4000})(req\.|req\.query|req\.body|req\.param)",
    ".*(res\.(write|send)\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*(res\.set\()(.{0,40000})(req\.|req\.query|req\.body|req\.param)",
    ".*{{{\s*[\w.\[\]\(\)]+\s*}}}",
    ".*{\s*[\w.\[\]\(\)]+\s*\|\s*s\s*}",
    ".*#{\s*[\w.\[\]\(\)\'\"]+\s*}",
    ".*&lt;%-\s*[\w.\[\]\(\)]+\s*%&gt;",
    ".*&lt;%-\s*@+[\w.\[\]\(\)]+\s*%&gt;",
    ".*require( )*(\()( *)('|\")request('|\")( *)(\))",
    ".*require( )*(\()( *)('|\")request('|\")( *)(\))",
    ".*require( )*(\()( *)('|\")needle('|\")( *)(\))",
    ".*require\(('|\")helmet-csp('|\")\)|helmet.csp|lusca.csp\(|Content-Security-Policy",
    ".*helmet.xframe|lusca.xframe\(|require\(('|\")frameguard('|\")\)|frameguard\(|X-Frame-Options",
    ".*helmet.hsts\({|lusca.hsts\({|hsts\({|require\(('|\")hsts('|\")\)|Strict-Transport-Security",
    ".*Public-Key-Pins(:|,)*",
    ".*helmet.xssFilter\(\)|lusca.xssProtection\(true\)|X-XSS-Protection('|\")*(\s)*(:|,)(\s)*('|\")*1",
    ".*helmet.noSniff|require\(('|\")dont-sniff-mimetype('|\")\)|nosniff\(\)|X-Content-Type-Options('|\")*(\s)*(:|,)(\s)*('\"\")*nosniff",
    ".*require\(('|\")ienoopen('|\")\)|ienoopen\(|helmet.ienoopen\(|X-Download-Options('|\")*(\s)*(:|,)(\s)*('\"\")*noopen",
    "httpOnly(\s)*:(\s)*true|httpOnly",
    ".disable\(('|\")x-powered-by('|\")\)|require\(('|\")hide-powered-by('|\")\)|hidePoweredBy\(|helmet.hidePoweredBy\(|removeHeader\(('|\")X-Powered-By('|\")\)"
]


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
    print beautyConsole.getColor("lightgrey") + _line + \
        beautyConsole.getSpecialChar("endline")


def build_file_list(start_dir):
    for subdir, dirs, files in os.walk(start_dir):
        for file in files:
            print os.path.join(subdir, file)


def main(src):
    """
    performs code analysis, line by line
    """
    global patterns_identified

    _file = open(src, "r")
    i = 0
    patterns_found_in_file = 0
    filenamelength = len(src)
    linelength = 97

    print "-" * 14, " FILE: \33[33m%s\33[0m " % src, "-" * \
        (linelength - filenamelength - 21)

    for _line in _file:
        i += 1
        __line = _line.strip()
        for __pattern in PATTERNS:
            __rex = re.compile(__pattern)
            if __rex.match(__line):
                patterns_found_in_file += 1
                printcodeline(_line, i, __pattern + ')',
                              ' dangerous pattern identified: ')

    if patterns_found_in_file < 1:
        print beautyConsole.getColor("green") + \
            "No patterns identified\n" + \
            beautyConsole.getSpecialChar("endline")
    else:
        patterns_identified = patterns_identified + patterns_found_in_file
        print "\n\n" + beautyConsole.getColor("red") + \
            "Identified %d code pattern(s)\n" % (patterns_found_in_file) + \
            beautyConsole.getSpecialChar("endline")
        print beautyConsole.getColor("white") + "-" * 100


# main program
if __name__ == "__main__":
    total_files = 0
    patterns_identified = 0

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
                        total_files = total_files + 1
        else:
            main(sys.argv[1])

        print


        # TODO summary by patter
        print beautyConsole.getColor("cyan")
        print " {} file(s) scanned in total".format(total_files)
        if patterns_identified > 0:
            print beautyConsole.getColor(
                "red"), "Identified {} code pattern(s) in total".format(patterns_identified)
        print beautyConsole.getColor("white")

    else:
        print "Enter JavaScript file name or directory name with file(s) to analyse"
        print "single file: ./nodestructor.py filename.js"
        print "directory: ./nodestructor.py -R dirname"
