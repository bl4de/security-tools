#!/usr/bin//env python3
### github.com/bl4de | hackerone.com/bl4de                      ###

import sys
import hashlib
import base64

description = """
hasher.py - hash string using SHA1, MD5, Base64, Hex, Encode URL etc.
usage: ./hasher.py [string_to_hash]
"""

colors = {
    "WHITE": '\33[37m',
    "GREEN": '\33[32m',
    "MAGENTA": '\33[35m',
    "CYAN": '\33[36m',
    "GREY": '\33[90m',
    "LIGHTGREY": '\33[37m'
}


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
    algorithms_available = ['md5', 'sha1', 'sha224', 'sha256', 'sha384',
                            'sha512', 'blake2s', 'blake2b']
    print(f"\n{colors['GREEN']}HASHES:{colors['WHITE']}\n")
    for h in algorithms_available:
        if hasattr(hashlib, h):
            try:
                h_method = getattr(hashlib, h)
                print(
                    f"{colors['GREY']}{h}\t\t{colors['CYAN']}{h_method(s.encode('utf-8')).hexdigest()}")
            except TypeError as e:
                pass
    print(f"\n{colors['GREEN']}ENCODE:{colors['WHITE']}\n")
    print(
        f"{colors['GREY']}Base64 \t\t{colors['CYAN']}{base64.b64encode(s.encode('utf-8'))}")
    print(
        f"{colors['GREY']}HEX encoded \t{colors['CYAN']}{hex_encode(s.encode('utf-8'))}")


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        arguments = sys.argv[1:]
        main(arguments[0])
    else:
        usage()
