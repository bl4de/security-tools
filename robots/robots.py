#!/usr/bin/python
#
# bl4de | <bloorq@gmail.com> | https://twitter.com/_bl4de
#
# robots.txt analyzer
# usage:
# ./robots.py [url]
#
import sys
import os

# TODO add reading folder with dirs

catalogs = ["admin",
            "log",
            "about",
            "manage",
            "manager",
            "panel"
            ]


def parse_robots(_res):
    for _line in _res.readlines():
        for c in catalogs:
            if c in _line:
                print "{} found!".format(c)


def main():
    _url = sys.argv[1]
    os.popen("rm -f robots.txt")
    os.popen("wget %s/robots.txt" % (_url))

    _res = file("robots.txt", "r")
    if _res:
        parse_robots(_res)

    print "analyze complete"


# main program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print "Enter url"
