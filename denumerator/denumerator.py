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
import argparse
import sys
import requests

welcome = """
--- dENUMerator ---
usage:
$ ./denumerator.py -f DOMAINS_LIST -t 5
"""


colors = {
    "white": '\33[37m',
    500: '\33[31m',
    200: '\33[32m',
    302: '\33[33m',
    304: '\33[33m',
    302: '\33[33m',
    401: '\33[94m',
    403: '\33[94m',
    404: '\33[94m',
    "magenta": '\33[35m',
    "cyan": '\33[36m',
    "grey": '\33[90m',
    "lightgrey": '\33[37m',
    "lightblue": '\33[94'
}

requests.packages.urllib3.disable_warnings()
allowed_http_responses = [200, 302, 304, 401, 404, 403, 500]
timeout = 2


def usage():
    """
    prints welcome message
    """
    print welcome


def send_request(proto, domain, output_file):
    """
    sends request to check if server is alive
    """
    protocols = {
        'http': 'http://',
        'https': 'https://'
    }
    resp = requests.get(protocols.get(proto.lower()) + domain,
                        timeout=timeout,
                        allow_redirects=False,
                        verify=False,
                        headers={'Host': domain})

    if resp.status_code in allowed_http_responses:
        print '[+] {}HTTP {}{}:\t {}'.format(
            colors[resp.status_code], resp.status_code, colors['white'], domain)

        if output_file:
            output_file.write('{}\n'.format(domain))
            output_file.flush()

    return resp.status_code


def enumerate_domains(domains, output_file, show=False):
    """
    enumerates domain from domains
    """
    for d in domains:
        try:
            d = d.strip('\n').strip('\r')
            return_code = send_request('http', d, output_file)
            # if http not working, try https
            if return_code not in allowed_http_responses:
                send_request('https', d, output_file)

        except requests.exceptions.InvalidURL:
            if show is True:
                print '[-] {} is not a valid URL :/'.format(d)
        except requests.exceptions.ConnectTimeout:
            if show is True:
                print '[-] {} :('.format(d)
            continue
        except requests.exceptions.ConnectionError:
            if show is True:
                print '[-] connection to {} aborted :/'.format(d)
        except requests.exceptions.ReadTimeout:
            if show is True:
                print '[-] {} read timeout :/'.format(d)
        except requests.exceptions.TooManyRedirects:
            if show is True:
                print '[-] {} probably went into redirects loop :('.format(d)
        else:
            pass


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", help="File with list of hostnames")
    parser.add_argument(
        "-t", "--timeout", help="Max. request timeout (default = 2)")
    parser.add_argument(
        "-s", "--success", help="Show all responses, including exceptions")
    parser.add_argument(
        "-o", "--output", help="Path to output file")

    args = parser.parse_args()
    if args.timeout:
        timeout = args.timeout

    if args.output:
        output_file = open(args.output, 'w+')
    else:
        output_file = False

    # set options
    show = True if args.success else False
    domains = open(args.file, 'rw').readlines()

    # main loop
    enumerate_domains(domains, output_file, show)
    
    # close output file
    if args.output:
        output_file.close()


if __name__ == "__main__":
    main()
