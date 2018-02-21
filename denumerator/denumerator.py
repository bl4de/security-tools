#!/usr/bin/env python
#pylint: disable=invalid-name
"""
--- dENUMerator ---

by bl4de | bloorq@gmail.com | Twitter: @_bl4de | HackerOne: bl4de

Enumerates list of subdomains (output from tools like Sublist3r or subbrute)
and creates output file with servers responding on port 80/HTTP

This indicates (in most caes) working webserver

usage:
$ ./denumerator.py [domain_list_file]
"""
from __future__ import print_function

import sys
import requests

welcome = """
--- dENUMerator ---
usage:
$ ./denumerator.py [domain_list_file]
"""

requests.packages.urllib3.disable_warnings()

allowed_http_responses = [200, 302, 304, 401, 404, 403, 500]


def usage():
    """
    prints welcome message
    """
    print(welcome)


def send_request(proto, domain):
    """
    sends request to check if server is alive
    """
    protocols = {
        'http': 'http://',
        'https': 'https://'
    }
    resp = requests.get(protocols.get(proto.lower()) + domain,
                        timeout=5,
                        allow_redirects=False,
                        verify=False,
                        headers={'Host': domain})

    if resp.status_code in allowed_http_responses:
        print('[+] domain {}:\t\t HTTP {}'.format(domain, resp.status_code))
        output_file.write('{}\n'.format(domain))
    return resp.status_code


def enumerate_domains(domains):
    """
    enumerates domain from domains
    """
    for d in domains:
        try:
            d = d.strip('\n').strip('\r')
            return_code = send_request('http', d)
            # if http not working, try https
            if return_code not in allowed_http_responses:
                send_request('https', d)

        except requests.exceptions.InvalidURL:
            print('[-] {} is not a valid URL :/'.format(d))
        except requests.exceptions.ConnectTimeout:
            print('[-] {} :('.format(d))
            continue
        except requests.exceptions.ConnectionError:
            print('[-] connection to {} aborted :/'.format(d))
        except requests.exceptions.ReadTimeout:
            print('[-] {} read timeout :/'.format(d))
        except requests.exceptions.TooManyRedirects:
            print('[-] {} probably went into redirects loop :('.format(d))
        else:
            pass


if len(sys.argv) < 2:
    print(welcome)
    exit(0)

domains = open(sys.argv[1].strip(), 'rw').readlines()
output_file = open('denumerator-{}-output.txt'.format(domains[0].strip()), 'w')

enumerate_domains(domains)

output_file.close()
