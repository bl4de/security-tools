#!/usr/bin/python
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
    print description
    exit(0)

def hex_encode(s):
    enc = ''
    for c in s:
        enc = enc + (str(hex(ord(c))).replace('0x',''))
    return enc


def main(s):
    print "SHA1\t\t{}".format(hashlib.sha1(s).hexdigest())
    print "MD5 \t\t{}".format(hashlib.md5(s).hexdigest())
    print "Base64 \t\t{}".format(base64.b64encode(s))
    print "URL-encoded \t{}".format(urllib.pathname2url(s))
    print "HEX encoded \t{}".format(hex_encode(s))


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        arguments = sys.argv[1:]
        main(arguments[0])
    else:
        usage()
