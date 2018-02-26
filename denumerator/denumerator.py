#!/usr/bin/python
# pylint: disable=invalid-name
"""
--- dENUMerator ---

by bl4de | bloorq@gmail.com | Twitter: @_bl4de | HackerOne: bl4de

Enumerates list of subdomains (output from tools like Sublist3r or subbrute)
and creates output file with servers responding on port 80/HTTP

This indicates (in most caes) working webserver

usage:
$ ./denumerator.py [domain_list_file]
"""

import sys
import requests

welcome = """
--- dENUMerator ---
usage:
$ ./denumerator.py [domain_list_file]
"""

requests.packages.urllib3.disable_warnings()

allowed_http_responses = [200, 302, 304, 401, 404, 403, 500]

http_ports_short_list = [80, 443, 8000, 8008, 8080, 9080]

http_ports_long_list = [80, 443, 591, 981, 1311, 4444,
              4445, 7001, 7002, 8000, 8008, 8080, 8088, 8222, 8530, 8531, 8887, 8888, 9080, 16080, 18091]


def usage():
    """
    prints welcome message
    """
    print welcome


def send_request(proto, domain, port=80):
    """
    sends request to check if server is alive
    """
    protocols = {
        'http': 'http://',
        'https': 'https://'
    }
    full_url = protocols.get(proto.lower()) + domain + ":" + str(port)
    resp = requests.get(full_url,
                        timeout=5,
                        allow_redirects=False,
                        verify=False,
                        headers={'Host': domain})

    if resp.status_code in allowed_http_responses:
        print '[+] domain {}:\t\t HTTP {}'.format(domain, resp.status_code)
        output_file.write('{}\n'.format(domain))
    return resp.status_code


def enumerate_domains(domains):
    """
    enumerates domain from domains
    """
    for d in domains:
        # TODO: make selection of port(s) list or pass as option:
        for port in http_ports_short_list:
            try:
                d = d.strip('\n').strip('\r')
                return_code = send_request('http', d, port)
                # if http not working on this port, try https
                if return_code not in allowed_http_responses:
                    send_request('https', d, port)

            except requests.exceptions.InvalidURL:
                print '[-] {} is not a valid URL :/'.format(d)
            except requests.exceptions.ConnectTimeout:
                print '[-] {} :('.format(d)
                continue
            except requests.exceptions.ConnectionError:
                print '[-] connection to {} aborted :/'.format(d)
            except requests.exceptions.ReadTimeout:
                print '[-] {} read timeout :/'.format(d)
            except requests.exceptions.TooManyRedirects:
                print '[-] {} probably went into redirects loop :('.format(d)
            else:
                pass


if len(sys.argv) < 2:
    print welcome
    exit(0)

domains = open(sys.argv[1].strip(), 'rw').readlines()
output_file = open('denumerator-{}-output.txt'.format(domains[0].strip()), 'w')

enumerate_domains(domains)

output_file.close()
