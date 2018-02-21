#!/usr/bin/env python

"""Web Application Fuzzer

"""
from __future__ import print_function
import requests
import os

url = "http://us.rd.yahoo.com/200/*http://google.ie*FUZZ"
fuzzString = "FUZZ"
counter = 0
separator = "#" * 80

os.system('clear')

print('[+] working, please be patient...')
for p in open('xss_vectors.txt', 'r').readlines():
    currentUrl = url.replace(fuzzString, p.strip()).strip()
    counter = counter + 1
    resp = requests.get(currentUrl)
    # print resp

    if resp.status_code in [200, 403, 500, 301, 302]:
        print('[+] {}  {}\n\n{}\n{}'.format(currentUrl, resp.status_code, resp.text, separator))

print('[+] Done')
