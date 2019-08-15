#!/usr/bin/env python3

### HTTP headers fuzzer
# args: url
import requests
import sys


def fuzz(u):
    print("[+] Fuzzing {}...".format(u))
    return

if __name__ == '__main__':
    u = sys.argv[1]
    fuzz(u)