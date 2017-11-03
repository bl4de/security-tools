#!/usr/bin/env python

### created by bl4de | bloorq@gmail.com | twitter.com/_bl4de    ###
### github.com/bl4de | hackerone.com/bl4de                      ###

import sys
import base64

description = """
baser.py - decode base64 file to plaintext
usage: ./baser.py [path_to_file_in_base64]

"""


def usage():
    print description
    exit(0)


def main(fname):
    f = open(fname, 'r').read()
    print f

    print "{}".format(base64.b64decode(f.strip()))


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        arguments=sys.argv[1:]
        main(arguments[0])
    else:
        usage()
