#!/usr/bin/python
#
# PHP exploitable functions searcher
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import sys

class colors:
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
    

def main():
    # open file to analyse
    _file = open(sys.argv[1], "r")
    i = 0
    total = 0
    
    for _line in _file:
        i = i + 1
        for _fn in exploitableFunctions:
            if _fn in _line:
                total = total + 1
                print "line %d : \33[33;1m%s()\33[0m found " % (i,_fn)
                print colors.Blue + _line + colors._endline
        
        
    if total < 1:
        print colors.Green + "No exploitable functions found" + colors._endline
    else:
        print colors.Red + "Found %d exploitable functions total" % (total) + colors._endline

# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        print
        print colors.Green + "------ PHP Exploitable functions scanner"
        print "------ GitHub: bl4de | Twitter: @_bl4de | bloorq@gmail.com"
        print
        print "------ file: \33[33m%s\33[0m " % (sys.argv[1])
        
        main()
        print
    else:
        print "Enter PHP file to analyse"