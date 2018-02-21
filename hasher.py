#!/usr/bin/python
### created by bl4de | bloorq@gmail.com | twitter.com/_bl4de    ###
### github.com/bl4de | hackerone.com/bl4de                      ###

from __future__ import print_function
import sys
import hashlib
import urllib
import base64

description = """
hasher.py - hash string using SHA1, MD5, Base64
usage: ./hasher.py [string_to_hash]

"""


def usage():
    print(description)
    exit(0)


def main(s):
    print("[+] SHA1\t\t{}".format(hashlib.sha1(s).hexdigest()))
    print("[+] MD5 \t\t{}".format(hashlib.md5(s).hexdigest()))
    print("[+] Base64 \t\t{}".format(base64.b64encode(s)))
    print("[+] URL-encoded \t{}".format(urllib.pathname2url(s)))


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        arguments = sys.argv[1:]
        main(arguments[0])
    else:
        usage()
