#!/usr/bin/python
#
# HTML source analyzer
#
import sys

_ident = "unknown"

def main():
    _file = open(sys.argv[1], "r")
    i = 0
    print "HTML Analyze"
    print "============"
    print
    for _line in _file:
        i = i + 1
        analyzeLine(_line, i)
        identify(_line)
    showStats(_file, i)
    

# using osftare recognition
def identify(_line):
    if "Jommla" in _line:
        _ident = "Joomla CMS"
    if "wp-content" in _line:
        _ident = "WordPress CMS"
        
    
def showStats(_file, i):
    print "\n------ SUMMARY -------\n"
    print "total lines of code: %d" % (i)
    print "identified software: %s" %(_ident)
    # end of summary
    print "\n"
    
# find interesting string(s)
def analyzeLine(_line, i):
    if "<!--" in _line:
        print "comment found at line %d: %s" % (i, _line.rstrip())
    if "admin" in _line:
        print "'admin' string found at line: %d" % (i)
    if "debug" in _line:
        print "debug information found at line %d" % (i)
    if "<script>" in _line:
        print "inline JavaScript found at line %d" % (i)
    if "\"/" in _line:
        print "possible directory path found at line %d" % (i)
    
# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print "Enter HTML file name"