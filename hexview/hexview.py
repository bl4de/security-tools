#!/usr/bin/python
"""
hexview.py - hex dump of any file

based on: "Tutorial: Making your own Hex Dump Program" by DrapsTV
https://www.youtube.com/watch?v=B8nRrw_M_nk&index=1&list=WL

"""
import argparse

COLORS = {
    "black": '\33[30m',
    "white": '\33[37m',
    "red": '\33[31m',
    "green": '\33[32m',
    "yellow": '\33[33m',
    "blue": '\33[34m',
    "magenta": '\33[35m',
    "cyan": '\33[36m',
    "grey": '\33[90m',
    "lightgrey": '\33[37m',
    "lightblue": '\33[94m'
}


def make_color(c):
    """
    Formats color for byte depends on if it's printable ASCII
    """
    # printable ASCII:
    if ord(c) < 128 and ord(c) > 32:
        retval = "{}{:02X}{}".format(COLORS['green'], ord(c), COLORS['white'])
    # non-printable ASCII
    else:
        retval = "{}{:02X}{}".format(COLORS['yellow'], ord(c), COLORS['white'])
    return retval


def format_text(c):
    """
    Formats color for character depends on if it's printable ASCII
    """
    if ord(c) < 128 and ord(c) > 32:
        retval = "{}{}{}".format(COLORS['green'], c, COLORS['white'])
    else:
        retval = "{}.{}".format(COLORS['yellow'], COLORS['white'])
    return retval


def format_chunk(chunk, start, stop, dec=False):
    """
    Formats one full chunk (byte)
    """
    if dec:
        return " ".join("{}:{}{:#04}{} ".format(make_color(c), COLORS['grey'],
                                                ord(c), COLORS['white']) for c in chunk[start:stop])
    else:
        return " ".join("{} ".format(make_color(c)) for c in chunk[start:stop])


def main():
    """
    main program routine
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Specify a file")
    parser.add_argument(
        "-d", "--decimal", help="Display DEC values with HEX", action="store_true")

    args = parser.parse_args()

    # b = args.opt_bytes or 16
    b = 16

    if args.file:
        offset = 0
        with open(args.file, 'rb') as infile:
            while True:
                chunk = infile.read(b)
                if len(chunk) == 0:
                    break

                text = str(chunk)
                text = ''.join([format_text(i) for i in text])

                output = "{}{:#08x}{}".format(
                    COLORS['cyan'], offset, COLORS['white']) + ": "

                output += format_chunk(chunk, 0, 4, args.decimal)
                output += " | "
                output += format_chunk(chunk, 4, 8, args.decimal)
                output += " | "
                output += format_chunk(chunk, 8, 12, args.decimal)
                output += " | "
                output += format_chunk(chunk, 12, 16, args.decimal)

                if len(chunk) % b != 0:
                    if args.decimal:
                        output += "   " * (((b * 2) - 4 - len(chunk))) + text
                    else:
                        output += "   " * (b - len(chunk)) + text
                else:
                    output += " " + text

                print output
                offset += 16
    else:
        print parser.usage


if __name__ == "__main__":
    main()
