#!/usr/bin/env python3
#
# PHP source code grep tool
# bl4de | github.com/bl4de | hackerone.com/bl4de
#

# pylint: disable=invalid-name, missing-class-docstring, import-error, too-few-public-methods, unused-import, no-self-use,missing-function-docstring,consider-using-enumerate,consider-iterating-dictionary

# @TODO:
# - allow to scan folder without subdirs
# - allow to scan files by pattern, eg. *.php
# - exclude 'echo' lines without HTML tags

## Sinks and Sources
#
# for an SQLi, you need a code that makes a raw query to the database
# for an SSRF, you need a code that makes an HTTP request
# for an LFI, you need a code that reads a file
# for an XXE, you need a code that parses an XML with a concrete configuration
# for a DOM-XSS, you need a code that executes HTML or JavaScript
#
# When you are going sources to sinks, the process is:
#
# - you encounter a function call
# - you find the definition
# - repeat until the sink
#
# For sinks to sources, the process is:
#
# - you are in the function definition
# - you find a call of this function.
# - repeat until the source
#

import sys
import os
import re
import argparse

from imports import pefdocs
from imports.beautyConsole import beautyConsole

# exploitable functions
exploitableFunctions = [
    "`",
    "system(",
    "exec(",
    "popen(",
    "pcntl_exec(",
    "eval(",
    "arse_str(",
    "parse_url(",
    "preg_replace(",
    "create_function(",
    "passthru(",
    "shell_exec(",
    "popen(",
    "proc_open(",
    "pcntl_exec(",
    "extract(",
    "putenv(",
    "ini_set(",
    "mail(",
    "unserialize(",
    "assert(",
    "call_user_func(",
    "call_user_func_array(",
    "ereg_replace(",
    "eregi_replace(",
    "mb_ereg_replace(",
    "mb_eregi_replace(",
    "virtual",
    "readfile(",
    "file_get_contents(",
    "show_source(",
    "highlight_file(",
    "fopen(",
    "file(",
    "fpassthru(",
    "fsockopen(",
    "gzopen(",
    "gzread(",
    "gzfile(",
    "gzpassthru(",
    "readgzfile(",
    "mssql_query(",
    "odbc_exec(",
    "sqlsrv_query(",
    "PDO::query(",
    "move_uploaded_file(",
    "echo",
    "print(",
    "printf(",
    "ldap_search(",
    "sqlite_",
    "sqlite_query(",
    "pg_",
    "pg_query(",
    "mysql_",
    "mysql_query(",
    "mysqli::query(",
    "mysqli_",
    "mysqli_query(",
    "apache_setenv(",
    "dl(",
    "escapeshellarg(",
    "escapeshellcmd(",
    "extract(",
    "get_cfg_var(",
    "get_current_user(",
    "getcwd(",
    "getenv(",
    "ini_restore(",
    "ini_set(",
    "passthru(",
    "pcntl_exec(",
    "php_uname(",
    "phpinfo(",
    "popen(",
    "proc_open(",
    "putenv(",
    "symlink(",
    "syslog(",
    "curl_exec(",
    "__wakeup(",
    "__destruct(",
    "__sleep(",
    "filter_var(",
    "file_put_contents(",
    "$_POST",
    "$_GET",
    "$_COOKIE",
    "$_REQUEST",
    "$_SERVER",
    "include($_GET",
    "require($_GET",
    "include_once($_GET",
    "require_once($_GET",
    "include($_REQUEST",
    "require($_REQUEST",
    "include_once($_REQUEST",
    "require_once($_REQUEST",
    "$_SERVER[\"PHP_SELF\"]",
    "$_SERVER[\"SERVER_ADDR\"]",
    "$_SERVER[\"SERVER_NAME\"]",
    "$_SERVER[\"REMOTE_ADDR\"]",
    "$_SERVER[\"REMOTE_HOST\"]",
    "$_SERVER[\"REQUEST_URI\"]",
    "$_SERVER[\"HTTP_USER_AGENT\"]",
    "SELECT.*FROM",
    "INSERT.*INTO",
    "UPDATE.*",
    "DELETE.*FROM"
]


def banner():
    """
    Prints welcome banner with contact info
    """
    print(beautyConsole.getColor("green") + "\n\n", "-" * 100)
    print("-" * 6, " PEF | PHP Exploitable Functions source code advanced grep utility",
          " " * 35, "-" * 16)
    print("-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ",
          " " * 22, "-" * 16)
    print("-" * 100, "\33[0m\n")


class PefEngine:
    """
    implements pef engine
    """

    def __init__(self, level, source_or_sink, filename, skip_vendor, phpfunction):
        """
        constructor
        """
        self.level = level  # scan only for level set of functions
        self.source_or_sink = source_or_sink  # show only sinks or sources
        self.filename = filename  # name of file/folder to scan
        self.skip_vendor = skip_vendor
        self.phpfunction = '' if phpfunction is None else phpfunction

        self.scanned_files = 0  # number of scanned files in total
        self.found_entries = 0  # total number of findings

        self.severity = {  # severity scale
            "high": 0,
            "medium": 0,
            "low": 0
        }

        self.header_printed = False
        return

    def analyse_line(self, l, i, fn, f, line):
        """
        analysis of single line of code; searches for pattern (passed as fn and atfn) occurence

        if occurence found, output is printed
        """
        res = None
        # there has to be space before function call; prevents from false-positives strings contains PHP function names
        atfn = f"@{fn}"
        fn = f"{fn}"
        # also, it has to checked agains @ at the beginning of the function name
        # @ prevents from output being echoed
        if fn in line or atfn in line:
            if fn == "`":
                res = self.print_code_line(
                    f.name, l, i, fn, self.severity, self.level, self.source_or_sink)
            else:
                res = self.print_code_line(
                    f.name, l, i, fn + (')' if '(' in fn else ''), self.severity, self.level, self.source_or_sink)
        return res

    def print_code_line(self, file_name, _line, i, fn, severity="", level='ALL', source_or_sink='ALL'):
        """
        prints formatted code line
        """
        impact_color = {
            "low": "green",
            "medium": "yellow",
            "high": "yellow",
            "critical": "red"
        }

        found = 0
        # print legend only if there i sentry in pefdocs.py

        if fn and fn.strip() in pefdocs.exploitableFunctionsDesc.keys():
            doc = pefdocs.exploitableFunctionsDesc.get(fn.strip())
            impact = doc[3]

            if (impact.upper() in level.upper()) or level == 'ALL':
                if self.phpfunction == '' or self.phpfunction in fn:
                    if (len(doc) == 5 and source_or_sink == doc[4]) or source_or_sink == 'ALL':
                        if len(_line) > 255:
                            _line = _line[:120] + \
                                    f" (...truncated -> line is {len(_line)} characters long)"
                        print("{}{}:{}\t{}{}{}{}".format(beautyConsole.getColor("white"), file_name, i,
                                                         beautyConsole.getColor(
                                                             impact_color[impact]),
                                                         beautyConsole.getColor(impact_color[impact]),
                                                         _line.strip()[:255],
                                                         beautyConsole.getColor("grey")))
                found += 1
            if impact not in severity.keys():
                severity[impact] = 1
            else:
                severity[impact] = severity[impact] + 1
            return found > 0

    def main(self, src):
        """
        main engine loop
        """
        f = open(str(src), "r", encoding="ISO-8859-1")
        i = 0
        res = None
        file_found = 0
        all_lines = f.readlines()
        for l in all_lines:
            i += 1
            line = l.rstrip()
            if self.level:
                if not self.is_comment(line):
                    for fn in exploitableFunctions:
                        if self.analyse_line(l, i, fn, f, line) == True:
                            res = True
                            file_found += 1
        return (res, file_found)  # return how many findings in current file

    def run(self):
        """
        runs scanning
        """
        total_found = 0
        os.system('clear')

        print(
            f"{beautyConsole.getColor('green')}>>> RESULTS <<<{beautyConsole.getColor('gray')}\n")

        if os.path.isdir(str(self.filename)):
            for root, _, files in os.walk(self.filename):
                if self.skip_vendor is True and "vendor" in root:
                    continue
                prev_filename = ""
                for f in files:
                    extension = f.split('.')[-1:][0]
                    if extension in ['php', 'inc', 'php3', 'php4', 'php5', 'phtml']:
                        self.scanned_files = self.scanned_files + 1
                        (res, file_found) = self.main(os.path.join(root, f))
                        if self.phpfunction == '' and res is not None and f != prev_filename:
                            print(f">>> {f} <<<\t{'-' * (115 - len(f))}\n\n")
                            prev_filename = f
                            total_found += file_found
        else:
            self.scanned_files = self.scanned_files + 1
            (res, self.found_entries) = self.main(self.filename)
        # print summary
        self.print_summary(total_found)

    def is_comment(self, line: str) -> bool:
        """
        If line is a comment, we should ignore it
        """
        line = re.sub(r"\s+", "", line)
        return line.startswith("/") or line.startswith("*")

    def print_summary(self, total_found: int) -> None:
        """
        prints summary at the bottom of search results
        """
        print(f"{beautyConsole.getColor('white')}Total issues found: {total_found}")
        print(
            f"\n{beautyConsole.getColor('grey')}Cmd arguments: {' '.join(sys.argv[1:])}\n")


# main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        add_help=True
    )
    filename = '.'  # initial value for file/dir to scan is current directory
    phpfunction = ''

    parser.add_argument(
        "-s", "--skip-vendor", help="exclude ./vendor folder", action="store_true")
    parser.add_argument(
        "-l", "--level", help="severity level: ALL, LOW, MEDIUM, HIGH or CRITICAL; default: ALL")
    parser.add_argument(
        "-S", "--source", help="show only sources", action="store_true")
    parser.add_argument(
        "-K", "--sink", help="show only sinks", action="store_true")
    parser.add_argument(
        "-f",
        "--function",
        help="Search for particular PHP function (eg. unserialize)",
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="Directory to scan (or sinlge file, optionally)",
    )

    args = parser.parse_args()

    level = args.level.upper() if args.level else 'ALL'
    source_or_sink = 'ALL'

    if args.source:
        source_or_sink = 'source'
    if args.sink:
        source_or_sink = 'sink'

    filename = args.dir

    # main orutine starts here
    engine = PefEngine(level, source_or_sink,
                       filename, args.skip_vendor, args.function)
    engine.run()
