#!/usr/bin/env python
# generates list of IP addresses from range IP start - IP stop
#
import sys

usage = """
### IP range address generator
### by bl4de | twiiter.com/_bl4de | hackerone.com/bl4de | github.com/bl4de

Generates list of IP addresses, starting from IP passed as first argument and ended up with 
IP address passed as second argument.

Sample usage: to generate all IPs between 192.168.1.1 and 192.168.2.255 (512 addresses):

./ip_generator.py 192.168.1.1 192.168.2.255

"""


def help():
    print usage


def generate(start, stop, logfile):
    for d in range(int(start[3]), int(stop[3]) + 1):
        for c in range(int(start[2]), int(stop[2]) + 1):
            for b in range(int(start[1]), int(stop[1]) + 1):
                for a in range(int(start[0]), int(stop[0]) + 1):
                    res = "{}.{}.{}.{}".format(a, b, c, d)
                    if logfile:
                        logfile.writelines("{}\n".format(res))
    return

if __name__ == "__main__":

    f = open("ip_list.log", "w+")

    if len(sys.argv) != 3:
        help()
        exit(0)

    start = sys.argv[1].split(".")
    stop = sys.argv[2].split(".")
    print "\n[+] generating IP addresses in range from {} to {}...".format(sys.argv[1], sys.argv[2])
    generate(start, stop, f)
    print "[+] addresses generated...\n"
    