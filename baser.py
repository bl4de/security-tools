#!/usr/bin/env python

### created by bl4de | bloorq@gmail.com | twitter.com/_bl4de    ###
### github.com/bl4de | hackerone.com/bl4de                      ###

from __future__ import print_function
import sys
import base64

DESC = """
baser.py - decode base64 file to plaintext
usage: ./baser.py [path_to_file_in_base64]

"""


def usage():
    """
    displays usage message
    """
    print(DESC)
    exit(0)


def main(fname):
    """
    decodes from Base64
    """
    __file = open(fname, 'r').read()
    print("{}".format(base64.b64decode(__file.strip())))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ARGS = sys.argv[1:]
        main(ARGS[0])
    else:
        usage()
