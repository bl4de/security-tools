#!/usr/bin/env python

"""Web Application Fuzzer

"""
import requests
import os

url = "https://my.chevrolet.com/FUZZ/"
fuzzString = "FUZZ"
counter = 0

os.system('clear')

print '[+] working, please be patient...'
for p in open('100.txt', 'r').readlines():
    currentUrl = url.replace(fuzzString, p.strip()).strip()
    counter = counter + 1
    resp = requests.get(currentUrl)
    # print resp

    if resp.status_code in [200, 403, 500, 301, 302]:
        print '[+] {}  {}'.format(currentUrl, resp.status_code)

print '[+] Done'
