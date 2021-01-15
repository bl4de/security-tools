#!/usr/bin/env python3
# Forked from https://gist.github.com/zPrototype/b211ae91e2b082420c350c28b6674170

import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target", "-t", action="store", help="Enter the target address", required=True)
parser.add_argument("--dest", "-d", action="store", help="Enter the address where you want to redirect to",
                    required=True)
parser.add_argument("--output", "-o", action="store", help="Enter output file name")
args = parser.parse_args()

payloads = []

# Remove protocol from url
junk = re.compile(r"https?://")
target = junk.sub("", args.target)
dest = junk.sub("", args.dest)

with open("payloads.txt", "r") as handle:
    templates = handle.readlines()

for payload in templates:
    payload = payload.rstrip()
    payload = re.sub("TARGET", target, payload)
    payload = re.sub("DEST", dest, payload)
    print(payload)
    payloads.append(payload)

if args.output:
    with open(args.output, "w")as handle:
        [handle.write(f"{x.rstrip()}\n") for x in payloads]