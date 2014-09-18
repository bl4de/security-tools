#!/usr/bin/python
#
# HTML source analyzer
#

def main():
    _file = open("index.html", "r")

    for _line in _file:
        print _line
        
# main program
if __name__ == "__main__":
    main()
