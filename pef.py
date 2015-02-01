#!/usr/bin/python
#
# PHP Exploitable Functions/Vars Scanner
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import sys
import os


class _PefOutput:
    def __init__(self):
        pass

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
    fiMsgFound = "file include pattern found; potential LFI/RFI detected"

# exploitable functions
exploitableFunctions = [" system", " exec", " popen", " pcntl_exec",
                        " eval", " preg_replace", " create_function", " include", " require", " passthru",
                        " shell_exec", " popen", " proc_open",
                        " pcntl_exec", " asset", " extract", " parse_str", " putenv", " ini_set", " mail", " header"]

# dangerous global(s)
globalVars = ["$_POST", "$_GET", "$_COOKIE", "$_REQUEST", "$_SERVER"]

# dangerous patterns - LFI/RFI
fileInclude = ["include($_GET", "require($_GET", "include_once($_GET", "require_once($_GET"]


# prints formated output line
def printcodeline(_line, i, _fn, _message):
    print "::  line %d :: \33[33;1m%s\33[0m %s found " % (i, _fn, _message)
    print _PefOutput.Blue + _line + _PefOutput._endline


# performs code analysis, line by line
def main(srcfile):
    # open file to analyse
    _file = open(srcfile, "r")
    i = 0
    total = 0
    filenamelength = len(srcfile)
    linelength = 97

    print "-" * 14, " FILE: \33[33m%s\33[0m " % srcfile, "-" * (linelength - filenamelength - 21), "\n"

    for _line in _file:
        i += 1
        __line = _line.replace(" ","")
        for _fn in exploitableFunctions:
            if _fn + '(' in __line or _fn + ' (' in __line:
                total += 1
                printcodeline(_line, i, _fn + '()', _PefOutput.efMsgFound)
        for _dp in fileInclude:
            if _dp in __line:
                total += 1
                printcodeline(_line, i, _dp + '()', _PefOutput.fiMsgFound)
        for _global in globalVars:
            if _global in __line:
                total += 1
                printcodeline(_line, i, _global, _PefOutput.efMsgGlobalFound)

    if total < 1:
        print _PefOutput.Green + "No exploitable functions found\n" + _PefOutput._endline
    else:
        print _PefOutput.Red + "Found %d exploitable functions total\n" % (total) + _PefOutput._endline

    print _PefOutput.White + "-" * 100

# main program
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        print _PefOutput.Green + "\n\n", "-" * 100
        print "-" * 6, " PEF | PHP Exploitable Functions scanner", " " * 35, "-" * 16
        print "-" * 6, " GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com ", " " * 22, "-" * 16
        print "-" * 100, "\33[0m\n"

        # main program loop
        if len(sys.argv) == 3 and sys.argv[1] == "-R":
            file_list = os.listdir(sys.argv[2])
            for __file in file_list:
                if os.path.isfile(__file) and '.php' in __file:
                    main(__file)
        else:
            main(sys.argv[1])

        print
    else:
        print "Enter PHP or directory name with file(s) to analyse"
        print "single file: pef filename.php"
        print "directory: pef -R dirname"