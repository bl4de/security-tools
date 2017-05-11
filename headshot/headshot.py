#!/usr/bin/env python

import requests
import sys


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


def response_description(resp):
    message = "[+] Sending {} request:  {} received {} {} with {} bytes of response {}"

    if resp.status_code != 200:
        return "{}[!] Sending {} request:  response size is {}; HTTP respone status is: {} {}{}".format(ConsoleOutputBeautifier.getColor('red'), method, resp_size, resp.status_code, resp.reason, ConsoleOutputBeautifier.getColor('white'))
    else:
        return message.format(method,
                              ConsoleOutputBeautifier.getColor(
                                  'green'), resp.status_code,
                              resp.reason, resp.headers.get(
                                  'content-length'),
                              ConsoleOutputBeautifier.getColor('white'))


if __name__ == "__main__":

    logfile = open("headshot.log", "w+")

    host = sys.argv[1]  # "dev.yahoo.companywebstores.com"

    formatted_request = """

    ---- REQUEST ----

    {} / HTTP/1.1
    Host: {}
    {}: {}

    ---- RESPONSE ----
    """

    base_response_size = 0

    # HTTP methods
    HTTP_METHODS = ['HEAD', 'GET', 'POST', 'OPTIONS', 'PUT', 'TRACE', 'DEBUG']

    # Headers payloads - piut any payload you want to test here:
    HEADERS_PAYLOADS = {
        'User-Agent': [
            '', '"', 'Fake', 'Fake' * 20, 'Mozilla'
        ]
    }

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
                    method, "https://" + host, headers=headers)

                prepared = session.prepare_request(req)
                resp = session.send(prepared)
                resp_size = resp.headers.get('content-length')
                base_response_size = resp_size if base_response_size == 0 else base_response_size
                print response_description(resp)
                logfile.write(formatted_request.format(
                    method, host, header, payload))
                logfile.write(response_description(resp))

    logfile.close()
    print "\n[+] DONE"
