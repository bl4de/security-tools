#!/usr/bin/python
#
# Python script skeleton
#

# module imports
# http://docs.python-requests.org/en/latest/user/quickstart/
import requests
import sys


def main(url):
    if 'http://' not in url:
        url = 'http://' + url

    req = requests.get(url)
    print req.headers


if __name__ == '__main__':
    url = sys.argv[1]

    main(url)