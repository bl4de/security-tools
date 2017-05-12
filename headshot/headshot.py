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

from modules.payloads import *

class ConsoleOutputBeautifier:
    """This class defines properties and methods to manipulate console output"""
    colors = {
        "black": '\33[30m',
        "white": '\33[37m',
        "red": '\33[31m',
        "green": '\33[32m',
        "yellow": '\33[33m',
        "blue": '\33[34m',
        "magenta": '\33[35m',
        "cyan": '\33[36m',
        "grey": '\33[90m',
        "lightblue": '\33[94'
    }

    characters = {
        "endline": '\33[0m'
    }

    def __init__(self):
        return None

    @staticmethod
    def getColor(color_name):
        """returns color identified by color_name or white as default value"""
        if color_name in ConsoleOutputBeautifier.colors:
            return ConsoleOutputBeautifier.colors[color_name]
        return ConsoleOutputBeautifier.colors["white"]

    @staticmethod
    def getSpecialChar(char_name):
        """returns special character identified by char_name"""
        if char_name in ConsoleOutputBeautifier.characters:
            return ConsoleOutputBeautifier.characters[char_name]
        return ""


def formatted_request(method, host, header, payload):
    return  """

    ---- REQUEST ----

    {} / HTTP/1.1
    Host: {}
    {}: {}

    ---- RESPONSE ----
    """.format(method, host, header, payload)


def line_start(fn):
    """
    line start decorator
    """
    def wrapper(*args, **kwargs):
        print "[+]"
        fn(*args, **kwargs)
    return wrapper


def response_description(resp):
    message = "[+] Sending {} request:  {} received {} {} with {} bytes of response {}"

    if resp.status_code != 200:
        return "[-] {}Sending {} request:  response size is {}; HTTP respone status is: {} {}{}".format(ConsoleOutputBeautifier.getColor('red'), method, resp_size, resp.status_code, resp.reason, ConsoleOutputBeautifier.getColor('white'))
    else:
        return message.format(method,
                              ConsoleOutputBeautifier.getColor(
                                  'green'), resp.status_code,
                              resp.reason, resp.headers.get(
                                  'content-length'),
                              ConsoleOutputBeautifier.getColor('white'))


if __name__ == "__main__":

    logfile = open("headshot.log", "w+")
    host = sys.argv[1]


    base_response_size = 0


    session = requests.Session()
    for method in HTTP_METHODS:
        for header in HEADERS_PAYLOADS:
            for payload in HEADERS_PAYLOADS[header]:
                headers = {
                    'Host': host,
                    header: payload
                }
                # print headers

                req = requests.Request(
                    method, "http://" + host, headers=headers)

                prepared = session.prepare_request(req)
                resp = session.send(prepared)
                resp_size = resp.headers.get('content-length')
                base_response_size = resp_size if base_response_size == 0 else base_response_size
                
                print response_description(resp)

                # save request/response to log file
                logfile.write(formatted_request(method, host, header, payload))
                logfile.write(response_description(resp))

    # done, wrap up and exit
    logfile.close()
    print "\n[+] DONE"
    exit(0)
