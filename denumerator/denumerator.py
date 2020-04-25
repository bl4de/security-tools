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
import subprocess
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
    <style>
        * {
            font-family: Verdana, Helvetica, Arial;
            font-size: 12px;
        }

        H4 {
            font-size: 14px;
            color: #777;
            font-weight: bold;
        }

        P {
            line-height: 1em;
            color:#121212;
        }

        TD {
            vertical-align: top;
            text-align: left;
            padding: 10px;
            border-top: 12px solid #6e6f6f;
        }
    </style>
</head>

<body>
    <table cellpadding="2" cellspacing="2">
    """
    html_output.write(html)
    return


def append_to_output(html_output, url, http_status_code, response_headers, nmap_output, ip_addresses):
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

    # IP address information
    ip_html = "<div>"
    ips = [ip for ip in ip_addresses.split(b"\n")]
    for ip in ips:
        if ip.find(b"address") > 0:
            ip_html = ip_html + "<p>IP: <strong style='font-size:15px;'>{}</strong></p>".format( ip.split(b"address")[1].decode("utf-8") )
    ip_html = ip_html + "</div>"

    # nmap scan results
    open_ports = [port for port in nmap_output.stdout.split(
        b"\n") if port.find(b"open") > 0]
    nmap_html = "<div>"
    for port in open_ports:
        nmap_html = nmap_html + \
            "<p style='font-weight: bold;'>{}</p>".format(port.decode("utf-8"))
    nmap_html = nmap_html + "</div>"

    # HTTP response headers
    response_headers_html = ""
    for header in response_headers.keys():
        response_headers_html = response_headers_html + "<p><strong>{}</strong> : {}</p>".format(
            header, response_headers[header]
        )

    html = """
        <tr>
            <td style="width:35%; margin-right:20px; border-right: 1px solid #0c0c0c;">
                <h4>HTTP Response Status: <strong style="color:#{};">{}</strong></h4>
                <p>
                    <a href="{}" target="_blank">{}</a>
                </p>
                <img style="width:360px; border:1px solid #cecece; margin:10px;" src="{}" />
            </td>

            <td style="width:35%; margin-right:20px; border-right: 1px solid #0c0c0c;"">
                <h4>HTTP Response Headers</h4>
                {}
            </td>
            
            <td>
                <h4>IP host addresses</h4>
                {}
                <hr>
                <h4>nmap scan results</h4>
                {}
            </td>
        </tr>
    """.format(http_status_code_color, http_status_code, url, url, screenshot_name, response_headers_html, ip_html, nmap_html)
    html_output.write(html)
    html_output.flush()
    return


def create_output_footer(html_output):
    html = """
            </table>
        </body>
    </html>
    """
    html_output.write(html)
    return


def send_request(proto, domain, output_file, html_output, allowed_http_responses, nmap_output, ip):
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
    if str(resp.status_code) in allowed_http_responses:
        print('[+] {}HTTP {}{}:\t {}'.format(
            colors[resp.status_code], resp.status_code, colors['white'], domain))

        if str(resp.status_code) in allowed_http_responses:
            append_to_output(html_output, protocols.get(
                proto.lower()) + domain, resp.status_code, resp.headers, nmap_output, ip)

        if output_file:
            output_file.write('{}\n'.format(domain))
            output_file.flush()

    return resp.status_code


def enumerate_domains(domains, output_file, html_output, allowed_http_responses, nmap_top_ports, show=False):
    """
    enumerates domain from domains
    """
    for d in domains:
        try:
            d = d.strip('\n').strip('\r')

            # IP address
            ip = subprocess.run(["host", d], capture_output=True).stdout
            
            # perform nmap scan
            nmap_output = subprocess.run(
                ["nmap", "--top-ports", str(nmap_top_ports), "-n", d], capture_output=True)
            print([port.decode("utf-8")
                   for port in nmap_output.stdout.split(b"\n") if port.find(b"open") > 0])

            send_request('http', d, output_file,
                         html_output, allowed_http_responses, nmap_output, ip)
            send_request('https', d, output_file,
                         html_output, allowed_http_responses, nmap_output, ip)

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
    allowed_http_responses = []

    parser.add_argument(
        "-f", "--file", help="File with list of hostnames")
    parser.add_argument(
        "-t", "--timeout", help="Max. request timeout (default = 2)")
    parser.add_argument(
        "-s", "--success", help="Show all responses, including exceptions")
    parser.add_argument(
        "-o", "--output", help="Path to output file")
    parser.add_argument(
        "-c", "--code", help="Show only selected HTTP response status codes, comma separated", default='200'
    )

    parser.add_argument(
        "-p", "--ports", help="--top-ports option for nmap (default = 100)", default=100
    )

    args = parser.parse_args()
    if args.timeout:
        timeout = args.timeout

    if args.output:
        output_file = open(args.output, 'w+')
    else:
        output_file = False

    if args.code:
        allowed_http_responses = args.code.split(',')
    else:
        allowed_http_responses = ['200']

    nmap_top_ports = args.ports

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
    enumerate_domains(domains, output_file, html_output,
                      allowed_http_responses, nmap_top_ports, show)

    # finish HTML output
    create_output_footer(html_output)
    html_output.close()

    # close output file
    if args.output:
        output_file.close()


if __name__ == "__main__":
    main()
