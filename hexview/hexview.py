#!/usr/bin/python
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Specify a file")
    parser.add_argument(
        "-o", "--output", help="Print outout to terminal", action="store_true")

    args = parser.parse_args()

    if args.file:
        offset = 0
        with open(args.file, 'rb') as infile:
            with open(args.file + ".dump", 'w') as outfile:
                while True:
                    chunk = infile.read(16)
                    if len(chunk) == 0:
                        break
                    
                    text = str(chunk)
                    print text
    else:
        print parser.usage
