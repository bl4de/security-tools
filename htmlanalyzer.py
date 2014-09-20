#!/usr/bin/python
#
# HTML source analyzer
#
import sys

def main():
    _file = open(sys.argv[1], "r")
    i = 0
    print "HTML Analyze"
    print "============"
    print
    for _line in _file:
        i = i + 1
        _analyzeLine(_line, i)
        
# find interesting string(s)
def _analyzeLine(_line, i):
    if "<!--" in _line:
        print "comment found at line %d: %s" % (i, _line)
    if "admin" in _line:
        print "'admin' string found at line: %d" % (i)
    if "debug" in _line:
        print "debug information found at line %d" % (i)
    
# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print "Enter HTML file name"