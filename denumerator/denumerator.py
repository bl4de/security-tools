#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
@TODO
- results summary
- disable/enable by HTTP Response Code (200/500/404/403/302)
- HTTP response headers


"""


"""
--- dENUMerator ---

by bl4de | bloorq@gmail.com | HackerOne: bl4de

Enumerates list of subdomains (output from tools like Sublist3r or subbrute)
and creates output file with servers responding on port 80/HTTP

This indicates (in most caes) working webserver

usage:
$ ./denumerator.py [domain_list_file]
"""
import argparse
import sys
import os
import time
import requests

welcome = """
--- dENUMerator ---
usage:
$ ./denumerator.py -f DOMAINS_LIST -t 5
"""


colors = {
    "white": '\33[37m',
    200: '\33[32m',
    204: '\33[32m',
    302: '\33[33m',
    304: '\33[33m',
    302: '\33[33m',
    401: '\33[94m',
    403: '\33[94m',
    404: '\33[94m',
    405: '\33[94m',
    415: '\33[94m',
    422: '\33[94m',
    500: '\33[31m',
    "magenta": '\33[35m',
    "cyan": '\33[36m',
    "grey": '\33[90m',
    "lightgrey": '\33[37m',
    "lightblue": '\33[94'
}

requests.packages.urllib3.disable_warnings()
allowed_http_responses = [200, 302, 403, 404, 405, 415, 422, 500]
# allowed_http_responses = [200]
timeout = 2

def usage():
    """
    prints welcome message
    """
    print(welcome)


def create_output_header(html_output):
    html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf8">
    <title>denumerator output</title>
</head>

<body>
    """
    html_output.write(html)
    return


def create_summary(html_output):
    html = """
    <div>
        <h4>Denumerator Summary</h4>
    </div>

    """
    html_output.write(html)


def append_to_output(html_output, url, http_status_code):
    screenshot_name = url.replace('https', '').replace(
        'http', '').replace('://', '') + '.png'
    screenshot_cmd = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --user-agent="bl4de/HackerOne" --disable-gpu --screenshot={} '.format(
        './report/' + screenshot_name)
    os.system(screenshot_cmd + url)

    # base color for all responses
    http_status_code_color = "000"

    # green - 200 OK
    if http_status_code == 200:
        http_status_code_color = "0c0"

    # red - error responses, but HTTP server exists
    if http_status_code in [403, 415, 422, 500]:
        http_status_code_color = "c00"

    html = """
<div style="padding:10px; border-top:1px solid #3e3e3e; margin-top:20px;">
    <h4>HTTP Response Status: <strong style="color:#{};">{}</strong></h4>
    <p>
        <a href="{}" target="_blank">{}</a>
    </p>
    <img style="width:360px; border:1px solid #cecece; margin:10px;" src="{}" />
</div>
    """.format(http_status_code_color, http_status_code, url, url, screenshot_name)
    html_output.write(html)
    html_output.flush()
    return


def create_output_footer(html_output):
    html = """
</body>
</html>
    """
    html_output.write(html)
    return


def send_request(proto, domain, output_file, html_output):
    """
    sends request to check if server is alive
    """
    protocols = {
        'http': 'http://',
        'https': 'https://'
    }

    print('\t--> {}{}'.format(protocols.get(proto.lower()), domain))

    resp = requests.get(protocols.get(proto.lower()) + domain,
                        timeout=timeout,
                        allow_redirects=False,
                        verify=False,
                        headers={'Host': domain})

    if resp.status_code in allowed_http_responses:
        print('[+] {}HTTP {}{}:\t {}'.format(
            colors[resp.status_code], resp.status_code, colors['white'], domain))

        if resp.status_code in allowed_http_responses:
            append_to_output(html_output, protocols.get(
                proto.lower()) + domain, resp.status_code)

        if output_file:
            output_file.write('{}\n'.format(domain))
            output_file.flush()

    return resp.status_code


def enumerate_domains(domains, output_file, html_output, show=False):
    """
    enumerates domain from domains
    """
    for d in domains:
        try:
            d = d.strip('\n').strip('\r')
            send_request('http', d, output_file, html_output)
            send_request('https', d, output_file, html_output)

        except requests.exceptions.InvalidURL:
            if show is True:
                print('[-] {} is not a valid URL :/'.format(d))
        except requests.exceptions.ConnectTimeout:
            if show is True:
                print('[-] {} :('.format(d))
            continue
        except requests.exceptions.ConnectionError:
            if show is True:
                print('[-] connection to {} aborted :/'.format(d))
        except requests.exceptions.ReadTimeout:
            if show is True:
                print('[-] {} read timeout :/'.format(d))
        except requests.exceptions.TooManyRedirects:
            if show is True:
                print('[-] {} probably went into redirects loop :('.format(d))
        except UnicodeError:
            pass
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
    domains = open(args.file, 'r').readlines()

    # create dir for HTML report
    if os.path.isdir('report') == False:
        os.mkdir('report')

    # starts output HTML
    html_output = open('report/__denumerator_report.html', 'w+')
    create_output_header(html_output)
    # main loop
    enumerate_domains(domains, output_file, html_output, show)

    # summary
    create_summary(html_output)
    
    # finish HTML output
    create_output_footer(html_output)
    html_output.close()

    # close output file
    if args.output:
        output_file.close()


if __name__ == "__main__":
    main()
