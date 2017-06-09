#!/usr/bin/env python

"""HTTP headers fuzzer
    bl4de | bloorq@gmail.com | Twitter: @_bl4de | HackerOne: bl4de

    headshot.py is HTTP headers fuzzer

    The idea is to provide easy way to quickly enumerate multiple combinations
    of HTTP methods and headers to catch weird server behaviour.

    Copyright 2017 bl4de

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

import requests
import sys
import numpy

from modules.payloads import *
from modules.utils import *

requests.packages.urllib3.disable_warnings()

def usage():
    usage = """
    Usage:

    $ ./headshot.py URL
    """
    print usage
    exit(0)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()
        
    logfile = open("headshot.log.html", "w+")
    host = sys.argv[1]

    base_response_size = 0

    session = requests.Session()
    for method in HTTP_METHODS:
        for header in HEADERS_PAYLOADS:
            for payload in HEADERS_PAYLOADS[header]:
                # print headers
                try:
                    headers = {
                        'Host': host.split('://')[1],
                        header: payload
                    }
                    req = requests.Request(method, host, headers=headers)
                    prepared = session.prepare_request(req)
                    
                    # print prepared.headers
                    # exit(0)
                    resp = session.send(prepared)
                    resp_size = resp.headers.get('content-length')
                    base_response_size = resp_size if base_response_size == 0 else base_response_size

                    print response_description(method, resp_size, resp)

                    # save request/response to log file
                    logfile.write(formatted_request(
                        method, host, header, payload))
                    logfile.write("\n{} {}\n".format(resp.status_code, resp.reason))
                    for h in resp.headers:
                        logfile.write('{}: {}\n'.format(h, resp.headers.get(h)))
                    
                    logfile.write("\n\n{}".format(resp.content))

                except requests.exceptions.ConnectTimeout:
                    print '[-] {} :('.format(d)
                    continue
                except requests.exceptions.ConnectionError:
                    print '[-] connection to {} aborted :/'.format(host)
                except requests.exceptions.ReadTimeout:
                    print '[-] {} read timeout :/'.format(host)
                except requests.exceptions.TooManyRedirects:
                    print '[-] {} probably went into redirects loop :('.format(host)
                    exit(0)
                else:
                    pass

    # done, wrap up and exit
    logfile.close()
    print "\n[+] DONE"
    exit(0)
