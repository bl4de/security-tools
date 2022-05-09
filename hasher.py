#!/usr/bin//env python3
### github.com/bl4de | hackerone.com/bl4de                      ###

import sys
import hashlib
import urllib
import base64

description = """
hasher.py - hash string using SHA1, MD5, Base64, Hex, Encode URL etc.
usage: ./hasher.py [string_to_hash]
"""


def usage():
    print(description)
    exit(0)


def hex_encode(s):
    enc = ''
    for c in s:
        enc = enc + (str(hex(c)).replace('0x', ''))
    return enc


def main(s):
    print("SHA1\t\t{}".format(hashlib.sha1(s.encode('utf-8')).hexdigest()))
    print("MD5 \t\t{}".format(hashlib.md5(s.encode('utf-8')).hexdigest()))
    print("Base64 \t\t{}".format(base64.b64encode(s.encode('utf-8'))))
    print("HEX encoded \t{}".format(hex_encode(s.encode('utf-8'))))


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        arguments = sys.argv[1:]
        main(arguments[0])
    else:
        usage()
