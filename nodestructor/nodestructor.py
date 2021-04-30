#!/usr/bin/env python3
#
# nodestructor
# Node.js application static code analysis tool
#
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
# pylint: disable=W1401
# pylint: disable=C
"""
nodestructor.py - static code analysis for Node.js applications
by bl4de
GitHub: bl4de | Twitter: @_bl4de | hackerone.com/bl4de  bloorq@gmail.com
"""

import os
import re
import argparse

from imports.beautyConsole import beautyConsole


banner = r"""

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

nodejs_patterns = [
    ".*url.parse\(",
    ".*[pP]ath.normalize\(",
    ".*fs.*File.*\(",
    ".*fs.*Read.*\(",
    ".*pipe\(res",
    ".*bodyParser\(",
    ".*eval\(",
    ".*exec\(",
    ".*execSync\(",
    ".*res.write\(",
    ".*child_process",
    ".*child_process.exec\(",
    ".*\sFunction\(",
    ".*execFile\(",
    ".*spawn\(",
    ".*fork\(",
    ".*setImmediate\(",
    ".*newBuffer\(",
    ".*\.constructor\("
]

npm_patterns = [
    ".*serialize\(",
    ".*unserialize\("
]

browser_patterns = [
    ".*urlsearchParams\(",
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
    ".*postMessage\(",
    ".*.addEventListener\(['\"]message['\"]",
    ".*.ajax\(",
    ".*.getJSON\(",
    ".*\$http\(",
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
    ".*\.dangerouslySetInnerHTML",
    ".*\.bypassSecurityTrust.*",
    ".*localStorage\.",
    ".*sessionStorage\.",
    ".*\$sce\.trustAsHtml\(",
    ".*\.load\(",
    ".*jQuery\.ajax\(",
    ".*parseHTML",
    ".*wrap.*\(",
    ".*html\(",
    ".*before\(",
    ".*after\(",
    ".*insertBefore\(",
    ".*insertAfter\(",
    ".*prepend",
    ".*setContent\(",
    ".*setHTML\(",
    ".*\.SafeString\("
]

url_regex = re.compile("(https|http):\/\/[a-zA-Z0-9#=\-\?\&\/\.]+")
urls = []

patterns = nodejs_patterns + npm_patterns
total_files = 0
patterns_identified = 0
files_with_identified_patterns = 0

minified_ext = ['.min.js']
SKIP_ALWAYS = ['package.json', 'README.md']
TEST_FILES = ['test.js', 'tests.js']
skip_node_modules = False
skip_test_files = False
identify_urls = False
exclude = []
exclude_always = ['babel', 'lodash', 'ansi', 'array', 'core-util', '.bin',
                  'babylon', 'next-tick',
                  'core-js', 'es5', 'es6', 'convert-source-map', 'source-map-',
                  'mime',
                  'to-fast-properties', 'json5', 'async', 'http-proxy',
                  'mkdirp', 'loose-envify',
                  '.git', '.idea']
include = []
pattern = ""
EXCLUDE_patterns = []


def show_banner():
    """
    Prints welcome banner with contact info
    """
    global banner
    print(beautyConsole.getColor("cyan"))
    print(banner)
    print(beautyConsole.getColor("white"))


def printcodeline(_line, i, _fn, _message, _code, verbose):
    """
    Formats and prints line of output
    """
    _fn = _fn.replace("*", "").replace("\\", "").replace(".(", '(')[0:len(_fn)]
    print("::  line %d :: \33[33;1m%s\33[0m %s " % (i, _fn, _message))

    if verbose:
        if i > 3:
            print(str(i - 3) + '   ' + beautyConsole.getColor("grey") + _code[i-3].rstrip() +
                  beautyConsole.getSpecialChar("endline"))
        if i > 2:
            print(str(i - 2) + '   ' + beautyConsole.getColor("grey") + _code[i-2].rstrip() +
                  beautyConsole.getSpecialChar("endline"))

        print(str(i) + '   ' + beautyConsole.getColor("green") + _line.rstrip() +
              beautyConsole.getSpecialChar("endline"))

        if i < len(_code) - 1:
            print(str(i + 1) + '   ' + beautyConsole.getColor("grey") + _code[i+1].rstrip() +
                  beautyConsole.getSpecialChar("endline"))
        if i < len(_code) - 2:
            print(str(i + 2) + '   ' + beautyConsole.getColor("grey") + _code[i+2].rstrip() +
                  beautyConsole.getSpecialChar("endline"))


def process_files(subdirectory, sd_files, pattern="", verbose=False):
    """
    recursively iterates ofer all files and checks those which meet
    criteria set by options only
    """
    global total_files
    for __file in sd_files:
        current_filename = os.path.join(subdirectory, __file)
        if current_filename[-3:] == '.js':
            if not '/node_modules/' in subdirectory or ('/node_modules/' in subdirectory and skip_node_modules is False):
                if (skip_test_files is False):
                    perform_code_analysis(current_filename, pattern, verbose)
                    total_files = total_files + 1
                else:
                    if __file not in TEST_FILES and "/test" not in current_filename and "/tests" not in current_filename:
                        perform_code_analysis(
                            current_filename, pattern, verbose)
                        total_files = total_files + 1


def perform_code_analysis(src, pattern="", verbose=False):
    """
    performs code analysis, line by line
    """
    global patterns
    global patterns_identified
    global files_with_identified_patterns

    # if -P / --pattern is defined, overwrite patterns with user defined
    # value(s)
    if pattern:
        patterns = [".*" + pattern]

    print_filename = True

    _file = open(src, "r")
    _code = _file.readlines()
    i = 0
    patterns_found_in_file = 0

    for _line in _code:
        i += 1
        __line = _line.strip()
        for __pattern in patterns:
            __rex = re.compile(__pattern)
            if __rex.match(__line.replace(' ', '')):
                if print_filename:
                    files_with_identified_patterns = files_with_identified_patterns + 1
                    print("FILE: \33[33m{}\33[0m\n".format(src))
                    print_filename = False
                patterns_found_in_file += 1
                printcodeline(_line, i, __pattern,
                              ' code pattern identified: ', _code, verbose)

            # URL searching
            if identify_urls == True:
                if url_regex.search(__line):
                    __url = url_regex.search(__line).group(0)
                    # show each unique URL only once
                    if __url not in urls:
                        printcodeline(__url, i, __url,
                                      ' URL found: ', _code, verbose)
                        urls.append(__url)

    if patterns_found_in_file > 0:
        patterns_identified = patterns_identified + patterns_found_in_file
        print(beautyConsole.getColor("red") +
              "\nIdentified %d code pattern(s)\n" % (patterns_found_in_file) +
              beautyConsole.getSpecialChar("endline"))
        print(beautyConsole.getColor("white") + "-" * 100)


# main program
if __name__ == "__main__":
    show_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Specify a file or directory to scan")
    parser.add_argument(
        "-r", "--recursive", help="check files recursively", action="store_true")
    parser.add_argument(
        "-v", "--verbose", help="verbose output - show code before/after vulnerable line", action="store_true")
    parser.add_argument(
        "-e", "--exclude", help="comma separated list of packages to exclude from scanning (eg. babel excludes ALL packages with babel in name, like babel-register, babel-types etc.")
    parser.add_argument(
        "-i", "--include", help="comma separated list of selected packages for scanning. Might be useful in projects where there are hundreds of dependiences and only some of them needs to be processed")
    parser.add_argument(
        "-s", "--skip-node-modules", help="when scanning recursively, do not scan ./node_modules folder", action="store_true")
    parser.add_argument(
        "-t", "--skip-test-files", help="when scanning recursively, do not check test files (usually test.js)", action="store_true")
    parser.add_argument(
        "-b", "--include-browser-patterns", help="include HTML patterns, like <a href=, <img src=, <iframe src= etc.", action="store_true")
    parser.add_argument(
        "-u", "--include-urls", help="identify URLs", action="store_true")
    parser.add_argument(
        "-p", "--pattern", help="define your own pattern to look for. Pattern has to be a RegEx, like '.*fork\('. nodestructor removes whiitespaces, so if you want to look for 'new fn()', your pattern should look like this: '.*newfn\(\)' (all special characters for RegEx have to be escaped with \ )")

    args = parser.parse_args()

    try:
        base_path = args.filename
        if args.recursive:
            FILE_LIST = os.listdir(args.filename)

        pattern = args.pattern if args.pattern else ""

        exclude = [e for e in args.exclude.split(
            ',')] + exclude_always if args.exclude else exclude_always
        include = [i for i in args.include.split(',')] if args.include else []

        skip_node_modules = args.skip_node_modules
        skip_test_files = args.skip_test_files
        identify_urls = args.include_urls
        verbose = args.verbose

        if args.include_browser_patterns:
            patterns = patterns + browser_patterns

        if args.recursive:
            for subdir, dirs, files in os.walk(base_path):
                if not include:
                    if not True in [e in subdir for e in exclude]:
                        process_files(subdir, files, pattern, verbose)
                else:
                    if True in [i in subdir for i in include]:
                        process_files(subdir, files, pattern, verbose)
        else:
            # process only single file
            s_filename = args.filename
            if s_filename[-3:] == '.js':
                perform_code_analysis(s_filename, pattern, verbose)
                total_files = total_files + 1

    except Exception as ex:
        print("{}An exception occured: {}\n\n".format(
            beautyConsole.getColor("red"), ex))
        exit(1)

    print(beautyConsole.getColor("cyan"))
    print(" {} file(s) scanned in total".format(total_files))
    if patterns_identified > 0:
        print(beautyConsole.getColor("red"))
        print("Identified {} code pattern(s) in {} file(s)".format(
            patterns_identified, files_with_identified_patterns))
    else:
        print(beautyConsole.getColor("green"), "No code pattern identified")
    print(beautyConsole.getColor("white"))
