#!/usr/bin/python
#
# Python script skeleton
#

# module imports
# http://docs.python-requests.org/en/latest/user/quickstart/
import requests
import sys


def main():
    url = sys.argv[1]
    rep = sys.argv[2]
    
    if 'http://' not in url:
        url = 'http://' + url
        
    if rep > 0:
        print rep
        while rep > 0:
            print "Request %d" % int(rep)
            req = requests.get(url)
            print req.headers
            rep=int(rep)-1
    

if __name__ == '__main__':
    main()