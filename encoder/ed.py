#!/usr/bin/env python
"""ED encoder/decoder tools
    bl4de | bloorq@gmail.com | Twitter: @_bl4de | H1: bl4de | GitHub: bl4de

    Simple encoder/decoder tool
    ./ed.py [string to encode] [input encoding] [output encoding]
"""
import base64
import sys
import urllib


def __get_char_hex_value(c):
    """returns 61; for 'a' truncated from 0x61"""
    return hex(ord(c)).replace("0x", "")


def to_base_64(s):
    return base64.b64encode(s)


def from_base_64(s):
    return base64.b64decode(s)


def url_encode(s):
    return urllib.quote(s)


def to_ascii(s):
    return s


def from_ascii(s):
    return s


def from_hex(s):
    xs = ""
    decimals = s.split()
    for d in decimals:
        xs += str(int(d, 10))

    return xs


def to_hex(s):
    xs = ""
    hexnums = s.split()
    for d in hexnums:
        hexnum = str(hex(int(d, 10))).replace("0x", "")
        if len(hexnum) < 2:
            hexnum = "0" + hexnum
        xs += hexnum + " "

    return xs


def to_html_entities(s):
    xs = ""
    for c in s:
        entity = "&#x00" + __get_char_hex_value(c) + ";"
        if entity:
            xs += entity
    return xs


if __name__ == "__main__":
    fn_map_from = {
        "base64": from_base_64,
        "ascii": from_ascii,
        "hex": from_hex
    }

    fn_map_to = {
        "base64": to_base_64,
        "ascii": to_ascii,
        "url": url_encode,
        "hex": to_hex,
        "html_entities": to_html_entities
    }

    if len(sys.argv) != 4:
        print "usage: ed.py [string] [input] [output]" \
              "\n\n input: base64, ascii, hex\n " \
              "output: base64, ascii, url, hex, html_entities ( eg. &#0022;)"
        exit(0)

    # f = open(sys.argv[1], "r")
    # # TODO remove special chars - arg passing
    # data = f.readline().replace("\\n", "")

    data = sys.argv[1]
    output = fn_map_from[sys.argv[2]](fn_map_to[sys.argv[3]](data))

    print output
