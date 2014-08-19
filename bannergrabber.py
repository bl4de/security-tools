#!/usr/bin/python
#
# Python script skeleton
#

# module imports
import socket

addr = ('127.0.0.1', 80)

# function definitons


def main():
    socket.setdefaulttimeout(2)
    s = socket.socket()
    try:
        s.connect(addr)
        ans = s.recv(1024)
        print ans
    except:
        print "Error, can't connect"

# main program
if __name__ == "__main__":
    main()
