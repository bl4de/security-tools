#!/usr/bin//env python3
### github.com/bl4de | hackerone.com/bl4de                      ###

import sys
import hashlib
import base64

description = """
hasher.py - hash string using SHA1, MD5, Base64, Hex, Encode URL etc.
usage: ./hasher.py [string_to_hash]
"""


def usage():
    '''
    prints usage info
    '''
    print(description)
    exit(0)


def hex_encode(s):
    '''
    HEX-encode string
    '''
    enc = ''
    for c in s:
        enc = enc + (str(hex(c)).replace('0x', ''))
    return enc


def main(s):
    '''
    prints all hashes for provided string
    '''
    algorithms_available = ['blake2s', 'blake2b', 'sha224',
                            'sha256', 'sha512', 'sha384', 'sha1', 'md5']
    print("\nHASH:\n")
    for h in algorithms_available:
        if hasattr(hashlib, h):
            try:
                h_method = getattr(hashlib, h)
                print(f"{h}\t\t{h_method(s.encode('utf-8')).hexdigest()}")
            except TypeError as e:
                pass
    print("\nENCODE:\n")
    print("Base64 \t\t{}".format(base64.b64encode(s.encode('utf-8'))))
    print("HEX encoded \t{}".format(hex_encode(s.encode('utf-8'))))


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        arguments = sys.argv[1:]
        main(arguments[0])
    else:
        usage()
