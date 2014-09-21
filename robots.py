#!/usr/bin/python
#
# HTML source analyzer
#
import sys
import os

def main():
    _url = sys.argv[1]
    _res = os.popen("wget -q %s/robots.txt" % (_url)).read()
    
    if "admin" in _res:
        print "'admin' catalog name found!"
    
    print "analyze complete"
        
# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print "Enter url"