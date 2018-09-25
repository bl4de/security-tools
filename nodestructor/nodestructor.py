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

import os
import re
import argparse

from imports.beautyConsole import beautyConsole


BANNER = """
                                                                    
                    (                )                    )           
                    )\ )   (      ( /( (      (        ( /(      (    
        (      (   (()/(  ))\ (   )\()))(    ))\   (   )\()) (   )(   
        )\ )   )\   ((_))/((_))\ (_))/(()\  /((_)  )\ (_))/  )\ (()\  
        _(_/(  ((_)  _| |(_)) ((_)| |_  ((_)(_))(  ((_)| |_  ((_) ((_) 
        | ' \))/ _ \/ _` |/ -_)(_-<|  _|| '_|| || |/ _| |  _|/ _ \| '_| 
        |_||_| \___/\__,_|\___|/__/ \__||_|   \_,_|\__|  \__|\___/|_|   
                                                                
#####    static code analysis for Node.js and other JavaScript apps        #####
#####    GitHub.com/bl4de | twitter.com/_bl4de | hackerone.com/bl4de       #####

example usages:   
            $ ./nodestructor filename.js
            $ ./nodestructor -R ./dirname
            $ ./nodestructor -R ./dirname --skip-node-modules --skip-test-files
            $ ./nodestructor -R ./node_modules --exclude=babel,lodash,ansi
            $ ./nodestructor -R ./node_modules --include=body-parser,chalk,commander
            $ ./nodestructor -R ./node_modules --pattern="obj.dangerousFn\("
"""

NODEJS_PATTERNS = [
    ".*url.parse\(",
    ".*[pP]ath.normalize\(",
    ".*fs.*File.*\(",
    ".*fs.*Read.*\(",
    ".*process.cwd\(",
    ".*pipe\(res",
    ".*bodyParser\(",
    ".*eval\(",
    ".*res.write\(",
    ".*child_process",
    ".*child_process.exec\(",
    ".*Function\(",
    ".*execFile\(",
    ".*spawn\(",
    ".*fork\(",
    ".*setTimeout\(",
    ".*setInterval\(",
    ".*setImmediate\(",
    ".*newBuffer\(",
    ".*constructor\("
]

NPM_PATTERNS = [
    ".*serialize\(",
    ".*unserialize\("
]

BROWSER_PATTERNS = [
    ".*URLSearchParams\(",
    ".*innerHTML",
    ".*innerText",
    ".*textContent",
    ".*outerHTML",
    ".*appendChild\(",
    ".*document.write\(",
    ".*document.location",
    ".*document.URL",
    ".*document.documentURI",
    ".*document.URLUnencoded",
    ".*document.baseURI",
    ".*document.referrer",
    ".*location.href",
    ".*location.search",
    ".*location.hash",
    ".*location.host",
    ".*location.pathname",
    ".*document.cookie",
    ".*history.pushState\(",
    ".*history.replaceState\(",
    ".*navigator.userAgent",
    ".*window.open\(",
    ".*window.postMessage\(",
    ".*.addEventListener\(['\"]message['\"]",
    ".*.ajax",
    ".*.getJSON",
    ".*\$http.",
    ".*navigator.sendBeacon\(",
    ".*\.add\(",
    ".*\.append\(",
    ".*\.after\(",
    ".*\.before\(",
    ".*\.html\(",
    ".*\.prepend\(",
    ".*\.replaceWith\(",
    ".*\.wrap\(",
    ".*\.wrapAll\(",
    ".*\.dangerouslytSetInnerHTML\(",
    ".*\.bypassSecurityTrust.*\(",
    ".*localStorage\.",
    ".*sessionStorage\.",
    ".*\$sce\.trustAsHtml\("
]

HTML_PATTERNS = [
    ".*<a.*href.*>",
    ".*<img.*src.*>",
    ".*<iframe.*src.*>"
]

URL_REGEX = re.compile("(https|http):\/\/[a-zA-Z0-9#=\-\?\&\/\.]+")
URLS = []

PATTERNS = NODEJS_PATTERNS + NPM_PATTERNS
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
IDENTIFY_URLS = False
EXCLUDE = []
EXCLUDE_ALWAYS = ['babel', 'lodash', 'ansi', 'array', 'core-util', '.bin',
                  'babylon', 'next-tick',
                  'core-js', 'es5', 'es6', 'convert-source-map', 'source-map-',
                  'mime',
                  'to-fast-properties', 'json5', 'async', 'http-proxy',
                  'mkdirp', 'loose-envify',
                  '.git', '.idea']
INCLUDE = []
PATTERN = ""
EXCLUDE_PATTERNS = []


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
    _fn = _fn.replace("*", "").replace("\\", "").replace(".(", '(')[0:len(_fn)]
    print "::  line %d :: \33[33;1m%s\33[0m %s " % (i, _fn, _message)
    print beautyConsole.getColor("grey") + _line + \
        beautyConsole.getSpecialChar("endline")


def process_files(subdirectory, sd_files, pattern=""):
    """
    recursively iterates ofer all files and checks those which meet 
    criteria set by options only
    """
    global TOTAL_FILES
    for __file in sd_files:
        current_filename = os.path.join(subdirectory, __file)
        if (current_filename[-3:] not in EXTENSIONS_TO_IGNORE
                and current_filename not in SKIP_ALWAYS
                and current_filename[-2:] not in EXTENSIONS_TO_IGNORE
                and current_filename[-7:] not in MINIFIED_EXT):

            if not '/node_modules/' in subdirectory or ('/node_modules/' in subdirectory and SKIP_NODE_MODULES is False):
                if (SKIP_TEST_FILES is False):
                    perform_code_analysis(current_filename, pattern)
                    TOTAL_FILES = TOTAL_FILES + 1
                else:
                    if __file not in TEST_FILES and "/test" not in current_filename and "/tests" not in current_filename:
                        perform_code_analysis(current_filename, pattern)
                        TOTAL_FILES = TOTAL_FILES + 1


def perform_code_analysis(src, pattern=""):
    """
    performs code analysis, line by line
    """
    global PATTERNS_IDENTIFIED
    global FILES_WITH_IDENTIFIED_PATTERNS
    global PATTERNS

    # if -P / --pattern is defined, overwrite PATTERNS with user defined
    # value(s)
    if pattern:
        PATTERNS = [".*" + pattern]

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
                printcodeline(_line[0:120] + "...", i, __pattern,
                              ' code pattern identified: ')

            # URL searching
            if IDENTIFY_URLS == True:
                if URL_REGEX.search(__line):
                    __url = URL_REGEX.search(__line).group(0)
                    # show each unique URL only once
                    if __url not in URLS:
                        printcodeline(__url, i, __url, ' URL found: ')
                        URLS.append(__url)

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
        "-I", "--include", help="comma separated list of selected packages for scanning. Might be useful in projects where there are hundreds of dependiences and only some of them needs to be processed")
    parser.add_argument(
        "-S", "--skip-node-modules", help="when scanning recursively, do not scan ./node_modules folder", action="store_true")
    parser.add_argument(
        "-T", "--skip-test-files", help="when scanning recursively, do not check test files (usually test.js)", action="store_true")
    parser.add_argument(
        "-H", "--include-html-patterns", help="include HTML patterns, like <a href=, <img src=, <iframe src= etc.", action="store_true")
    parser.add_argument(
        "-U", "--include-urls", help="identify URLs", action="store_true")
    parser.add_argument(
        "-P", "--pattern", help="define your own pattern to look for. Pattern has to be a RegEx, like '.*fork\('. nodestructor removes whiitespaces, so if you want to look for 'new fn()', your pattern should look like this: '.*newfn\(\)' (all special characters for RegEx have to be escaped with \ )")

    ARGS = parser.parse_args()

    try:
        BASE_PATH = ARGS.filename
        if ARGS.recursive:
            FILE_LIST = os.listdir(ARGS.filename)

        PATTERN = ARGS.pattern if ARGS.pattern else ""

        EXCLUDE = [e for e in ARGS.exclude.split(
            ',')] + EXCLUDE_ALWAYS if ARGS.exclude else EXCLUDE_ALWAYS
        INCLUDE = [i for i in ARGS.include.split(',')] if ARGS.include else []

        SKIP_NODE_MODULES = ARGS.skip_node_modules
        SKIP_TEST_FILES = ARGS.skip_test_files
        IDENTIFY_URLS = ARGS.include_urls

        if ARGS.include_html_patterns:
            PATTERNS = PATTERNS + HTML_PATTERNS + BROWSER_PATTERNS

        if ARGS.recursive:
            for subdir, dirs, files in os.walk(BASE_PATH):
                if not INCLUDE:
                    if not True in [e in subdir for e in EXCLUDE]:
                        process_files(subdir, files, PATTERN)
                else:
                    if True in [i in subdir for i in INCLUDE]:
                        process_files(subdir, files, PATTERN)
        else:
            # process only single file
            S_FILENAME = ARGS.filename
            if (S_FILENAME[-3:] not in EXTENSIONS_TO_IGNORE
                and S_FILENAME[-2:] not in EXTENSIONS_TO_IGNORE
                    and S_FILENAME[-7:] not in MINIFIED_EXT):
                perform_code_analysis(S_FILENAME, PATTERN)
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
