#!/usr/bin/python
#
# REST API bubgounty tool
#
# bl4de <bloorq@gmail.com> | twitter.com/_bl4de | hackerone.com/bl4de | github.com/bl4de


### @TODO
### - colorful output based on HTTP Response code, content etc.
### - arguments parser
### - recursive paths, eg.:  /news  -> /news/add, /news/delete etc.
### - save output to file
### - ???

import requests

# make script arguments from these here:
HOSTNAME = 'af.opera.com'
api_url = HOSTNAME + '/api/'
USER_AGENT = 'bl4de/HackerOne'
SCHEMA = 'https://'
be_verbose = False


# HTTP methods
HTTP_METHODS = [
    'HEAD',
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'TRACE',
    'FAKE'
]

JSON_PAYLOAD = '{"user": "1", "role": "admin", "debug": "true", \
                 "verbose": "true", "": "", "key_no_value": "", "": "value_no_key"}'

XML_PAYLOAD = """
<?xml version="1.0"?>
<root>
    <user>Admin</user>
    <role>admininstartor</role>
    <debug>true</debug>
    <verbose>1</verbose>
    <empty></empty>
</root>
"""


HEADERS = {
    "Host": HOSTNAME,
    "User-Agent": USER_AGENT,
    "Accept": "*/*"
}

api_url = SCHEMA + api_url


def print_response(url, method, resp, msg=""):
    global be_verbose

    print "{} to {} {}: HTTP {}; \t\t\t\tresponse size: {}".format(
        method, url, resp.status_code, msg, len(resp.content))
    if be_verbose == True and len(resp.content) > 0:
        print "-- Response content --" + "-"*78
        print "\n{}\n".format(resp.content)
        print "\n" + "-"*100 + "\n"


def enumerate_endpoints(api_url, wordlist):
    print "[+] enumerating existing endpoints using dictionary..."
    c = 0
    enumerated = []
    for w in wordlist:
        resp = requests.get(api_url + w, headers=HEADERS)
        if resp.status_code != 404:
            enumerated.append(w)
            c = c + 1

    if c == 0:
        print "[-] no valid endpoints found at this url. Not much more can be done, so quitting now :/\n"
        exit(0)

    print "[+] done! Found {} valid endpoints.".format(c)
    return enumerated


def send_requests(enumerated_endpoints):
    print "[+] sending HTTP requests to previously identified {} endpoints. This migth take a while...\n\n".format(
        len(enumerated_endpoints))

    c = 0
    for http_method in HTTP_METHODS:
        if http_method == 'GET':

            get_params = [
                'debug',
                'test',
                't',
                'a'
            ]

            for w in enumerated_endpoints:
                c = c + 1
                resp = requests.get(api_url + w, headers=HEADERS)
                print_response(api_url + w, http_method, resp)

            for w in enumerated_endpoints:
                for param in get_params:
                    c = c + 1
                    url = api_url + w + '?{}=somedata'.format(param)
                    resp = requests.get(url, headers=HEADERS)
                    print_response(url, http_method, resp)

        if http_method == 'HEAD':
            for w in enumerated_endpoints:
                c = c + 1
                resp = requests.head(api_url + w, headers=HEADERS)
                print_response(api_url + w, http_method, resp)

        if http_method == 'POST':
            for w in enumerated_endpoints:
                c = c + 2
                # application/xml
                HEADERS['Content-Type'] = 'application/xml'
                resp = requests.post(
                    api_url + w, headers=HEADERS, data=XML_PAYLOAD)
                print_response(api_url + w, http_method,
                               resp,  " with XML payload")

                # application/json
                HEADERS['Content-Type'] = 'application/json'
                resp = requests.post(
                    api_url + w, headers=HEADERS, data=JSON_PAYLOAD)
                print_response(api_url + w, http_method,
                               resp,  " with JSON payload")

        if http_method == 'PUT':
            for w in enumerated_endpoints:
                c = c + 2
                # application/xml
                HEADERS['Content-Type'] = 'application/xml'
                resp = requests.put(
                    api_url + w, headers=HEADERS, data=XML_PAYLOAD)
                print_response(api_url + w, http_method,
                               resp, " with XML payload")

                # application/json
                HEADERS['Content-Type'] = 'application/json'
                resp = requests.put(
                    api_url + w, headers=HEADERS, data=JSON_PAYLOAD)
                print_response(api_url + w, http_method,
                               resp, " with JSON payload")

    print "[+] done! Total {} requests send.\n\n".format(c)


def main():
    wordlist = [
        'query',
        'user',
        'upload',
        'test',
        'debug',
        'check',
        'login'
    ]

    enumerated_endpoints = enumerate_endpoints(api_url, wordlist)
    send_requests(enumerated_endpoints)


if __name__ == "__main__":
    main()
