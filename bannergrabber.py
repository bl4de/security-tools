#!/usr/bin/python
#
# Python script skeleton
#

# module imports
import httplib
conn = httplib.HTTPConnection("localhost")
conn.request("GET", "/")
r1 = conn.getresponse()

print r1.getheaders()

# for i in dir(r1):
    # print i