#!/usr/bin/python
#
# PHP exploitable functions searcher
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import sys

class Colors:
    Black = '\33[30m'
    Red = '\33[31m'
    Green = '\33[32m'
    Yellow = '\33[33m'
    Blue ='\33[34m'
    Magenta = '\33[35m'
    Cyan = '\33[36m'
    White = '\33[37m'
    _endline = '\33[0m'

exploitableFunctions = ["system","exec","popen","backtick operator""pcntl_exec",
"eval","preg_replace","create_function", "include","require","passthru","shell_exec","`","popen","proc_open","pcntl_exec","asset","extract","parse_str","putenv","ini_set","mail","header"]

globalVars = ["$_POST", "$_GET", "$_COOKIE", "$_REQUEST", "$_SERVER"];

def printSrcCodeLine(_line, i, _fn):
    print "line %d : \33[33;1m%s\33[0m found " % (i,_fn)
    print Colors.Blue + _line + Colors._endline
    
def main():
    # open file to analyse
    _file = open(sys.argv[1], "r")
    i = 0
    total = 0
    
    for _line in _file:
        i = i + 1
        for _fn in exploitableFunctions:
            if _fn + '(' in _line or _fn + ' (' in _line:
                total = total + 1
                printSrcCodeLine(_line, i, _fn + '()')
        for _global in globalVars:
            if _global in _line:
                total = total + 1
                printSrcCodeLine(_line, i, _global)
        
    if total < 1:
        print
        print Colors.Green + "No exploitable functions found" + Colors._endline
    else:
        print
        print Colors.Red + "Found %d exploitable functions total" % (total) + Colors._endline

# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        print
        print
        print Colors.Green + "------ PHP Exploitable functions scanner"
        print "------ GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com"
        print
        print "------ file: \33[33m%s\33[0m " % (sys.argv[1])
        
        main()
        print
    else:
        print "Enter PHP file to analyse"