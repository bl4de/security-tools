#!/usr/bin/env python

"""
Automate tasks for full recon the target

Dependiences:

sublist3r       https://github.com/aboul3la/Sublist3r


Executed step(s) and used tools:

1. Enumerate subdomain(s) [sublist3r]
2.

"""

import sys
import subprocess

DOMAIN = ""
OUTPUT = open("OUTPUT", "w+")


def sublist3r(__args=[]):
    try:
        subprocess.Popen(['sublist3r', '--domain', DOMAIN, '--output', 'OUTPUT'])
    except:
        print "[-] sublist3r: missing domain name"
        exit(0)


def print_banner():
    """
    prints welcome banner
    """
    print "#####  Sword | by bl4de  #####\n\n"


def print_usage():
    """
    prints usage
    """
    print "usage: ./sword.py [domain] [steps] [exclude_tool(s)]\n\n"


def run(__task, __args):
    """
    task runner
    """
    try:
        __task(__args)
    except:
        print "[-] something went wrong :("
        exit(0)


# main program
if __name__ == "__main__":
    try:
        print sys.argv[1]
        if sys.argv[1]:
            DOMAIN = sys.argv[1]

        # subdomain(s) enumeration
        run(sublist3r, [DOMAIN])

    except:
        print "[-] missing DOMAIN, nothing to see here, move along..."
        exit(0)
