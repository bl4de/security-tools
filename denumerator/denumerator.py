#!/usr/bin/env python
# pylint: disable=invalid-name
"""
@TODO
- results summary
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
import json
import os
import subprocess
import time
from datetime import datetime

import requests

welcome = """
--- dENUMerator ---
usage:
$ ./denumerator.py -f DOMAINS_LIST -t 5
"""

DEFAULT_DIRECTORY = 'report'

colors = {
    "white": '\33[37m',
    200: '\33[32m',
    204: '\33[32m',
    206: '\33[32m',
    301: '\33[33m',
    302: '\33[33m',
    303: '\33[33m',
    304: '\33[33m',
    401: '\33[94m',
    403: '\33[94m',
    404: '\33[94m',
    405: '\33[94m',
    411: '\33[94m',
    412: '\33[94m',
    415: '\33[94m',
    422: '\33[94m',
    429: '\33[94m',
    500: '\33[31m',
    "magenta": '\33[35m',
    "cyan": '\33[36m',
    "grey": '\33[90m',
    "lightgrey": '\33[37m'
}
requests.packages.urllib3.disable_warnings()

timeout = 2
nmap = True
element_class_name_iterator = 1


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

        BODY {
            margin:0px;
        }

        DIV#header {
            position: fixed; 
            padding-left: 30px;
            top: 0px; 
            height:70px; 
            width: 100%; 
            background-color:#09a; 
            border-bottom:2px solid #ccc;
        }

        DIV#container {
            margin-top:100px; 
            width: 100%; 
            padding:10px;
            text-align:center;
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
        }

        TD.boundary {
            border-top: 5px solid #6e6f6f;
            border-bottom: 2px solid #6e6f6f;
            padding-left: 20px;
            background-color: #fafff4;
        }

        .fold {
            display: none;
        }

        .unfold {
            display: block;
            background-color: #f9f9db;
        }

        TR.visible {
            display: block;
        }

        TR.hidden {
            display: none;
        }
        
        A.toggle {
            margin-left:30px; 
            font-size: 18px;
            font-weight:bold;
            cursor: pointer;
            padding:5px 20px;
            border:1px solid #dadede;
            
            border-radius: 10px;
        }

        A.off {
            background-color: #f1f1fa;
        }

        A.on {
            background-color: #c4f3c5;
        }

        A.url {
            font-weight: bold;
            font-size:16px;
            text-decoration:none;
            margin-left: 120px;
        }
    </style>
</head>

<body>

    <script>
        function toggleFold(className, evtTarget = null) {
            const elements = document.getElementsByClassName(className);
            if (elements.length > 0) {
                [].forEach.call(elements, element => {
                    if (element.classList.contains('fold')) {
                        element.classList.remove('fold');
                        element.classList.add('unfold');
                        if (evtTarget) {
                            evtTarget.classList.remove('off');
                            evtTarget.classList.add('on');
                        } 
                    } else {
                        element.classList.remove('unfold');
                        element.classList.add('fold');
                        if (evtTarget) {
                            evtTarget.classList.remove('on');
                            evtTarget.classList.add('off');
                        } 
                    }
                });
            }
        }
        
        
        function showOnly(className, evtTarget = null) {
            const elements = document.getElementsByClassName(className);
            if (elements.length > 0) {
                [].forEach.call(elements, element => {
                    if (element.classList.contains('hidden')) {
                        element.classList.remove('hidden');
                        element.classList.add('visible');
                        if (evtTarget) {
                            evtTarget.classList.remove('off');
                            evtTarget.classList.add('on');
                        } 
                    } else {
                        element.classList.remove('visible');
                        element.classList.add('hidden');
                        if (evtTarget) {
                            evtTarget.classList.remove('on');
                            evtTarget.classList.add('off');
                        } 
                    }
                });
            }
        }
    </script>

    <div id="header">
        <p>
            <h6>Show: 
                <a onclick="showOnly('http_code_2_main', this);" class="toggle off" style="color:#0c0;">2xx </a>
                <a onclick="showOnly('http_code_3_main', this);" class="toggle off" style="color:#000;">3xx</a>
                <a onclick="showOnly('http_code_4_main', this);" class="toggle off" style="color:#c00;">4xx</a>
                <a onclick="showOnly('http_code_5_main', this);" class="toggle off" style="color:#c00;">5xx</a>
            </h6>
        </p>
    </div>

    <div id="container" style="margin-top:100px; width: 100%; padding:10px;">
        <table cellpadding="2" cellspacing="2">
    """
    html_output.write(html)
    return


def append_to_output(html_output, url, http_status_code, response_headers, nmap_output, ip_addresses, output_directory):
    global element_class_name_iterator

    screenshot_name = url.replace('https', '').replace(
        'http', '').replace('://', '') + '.png'
    screenshot_cmd = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --user-agent="HackerOne" --disable-gpu --dns-prefetch-disable --log-level=0 --timeout=30000 --virtual-time-budget=999999 --run-all-compositor-stages-before-draw --screenshot={} '.format(
        './reports/{}/'.format(output_directory) + screenshot_name)

    # os.system(screenshot_cmd + url)
    subprocess.run(
        screenshot_cmd + url,
        shell=True,
        timeout=30
    )

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
            ip_html = ip_html + "<p>IP: <strong style='font-size:15px;'>{}</strong></p>".format(
                ip.split(b"address")[1].decode("utf-8"))
    ip_html = ip_html + "</div>"

    nmap_html = "<div>"
    if nmap == True:
        # nmap scan results
        open_ports = [port for port in nmap_output.stdout.split(
            b"\n") if port.find(b"open") > 0]
        for port in open_ports:
            nmap_html = nmap_html + \
                        "<p style='font-weight: bold;'>{}</p>".format(
                            port.decode("utf-8"))
    nmap_html = nmap_html + "</div>"

    # HTTP response headers
    response_headers_html = ""
    for header in response_headers.keys():
        response_headers_html = response_headers_html + "<p style='width: 720px; overflow-wrap: break-word;'><strong>{}</strong> : {}</p>".format(
            header, response_headers[header]
        )
    element_class_name = 'result_{}'.format(element_class_name_iterator)
    element_class_name_iterator += 1

    html = """
        <tr class="http_code_{}_main">
            <td colspan="3" class="boundary">
                <h4>
                    HTTP Response Status: <strong style="font-size:18px; color:#{}; cursor:pointer;" onclick="toggleFold('{}', this);">{}</strong> 
                    <a class="url" href="{}" target="_blank">{}</a>
                </h4>
            </td>
        </tr>
        <tr class="http_code_{} {} fold">
            <td style="width:35%; margin-right:20px; border-right: 1px solid #0c0c0c; width:480px;">
                <a href="{}" target="_blank" title="Click to open fullsize screenshot in new tab">
                    <img style="width:360px; border:1px solid #cecece; margin:10px;" src="{}" />
                </a>
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
    """.format(
        (http_status_code // 100),
        http_status_code_color,
        element_class_name,
        http_status_code,
        url,
        url,
        (http_status_code // 100),
        element_class_name,
        screenshot_name,
        screenshot_name,
        response_headers_html,
        ip_html,
        nmap_html
    )
    html_output.write(html)
    html_output.flush()
    return


def create_output_footer(html_output):
    html = """
                </table>
            </div>
        </body>
    </html>
    """
    html_output.write(html)
    return


def send_request(proto, domain, output_file, html_output, allowed_http_responses, nmap_output, ip, output_directory):
    """
    sends request to check if server is alive
    """
    protocols = {
        'http': 'http://',
        'https': 'https://'
    }

    print('\t--> {}{}{}{}'.format(colors['magenta'], protocols.get(proto.lower()), domain, colors['white']))

    resp = requests.get(protocols.get(proto.lower()) + domain,
                        timeout=timeout,
                        allow_redirects=False,
                        verify=False,
                        headers={'Host': domain})
    if str(resp.status_code) in allowed_http_responses:
        print('[+] {} {}HTTP {}{}:\t {}'.format(
            datetime.now().strftime("%H:%M:%S"), colors[resp.status_code], resp.status_code, colors['white'], domain))

        if str(resp.status_code) in allowed_http_responses:
            append_to_output(html_output, protocols.get(
                proto.lower()) + domain, resp.status_code, resp.headers, nmap_output, ip, output_directory)

        if output_file:
            output_file.write('{}\n'.format(domain))
            output_file.flush()

    return resp.status_code


def enumerate_domains(domains, output_file, html_output, allowed_http_responses, nmap_top_ports, output_directory,
                      show=False):
    """
    enumerates domain from domains
    """
    iterator = 0
    number_of_domains = len(domains)
    for d in domains:
        iterator = iterator + 1
        try:
            d = d.strip('\n').strip('\r')
            print('\n{}[+] Checking domain {} from {}...{}'.format(colors['grey'],
                                                                   iterator, number_of_domains, colors['white']))
            # IP address
            ip = subprocess.run(
                ["host", d], capture_output=True, timeout=15).stdout
            nmap_output = ''

            if nmap == True:
                # perform nmap scan
                nmap_output = subprocess.run(
                    ["nmap", "--top-ports", str(nmap_top_ports), "-n", d], capture_output=True)
                print('{}  nmap: '.format(colors['grey']), [port.decode("utf-8")
                                                            for port in nmap_output.stdout.split(b"\n") if
                                                            port.find(b"open") > 0], '{}'.format(colors['white']))

            send_request('http', d, output_file,
                         html_output, allowed_http_responses, nmap_output, ip, output_directory)
            time.sleep(1)

            send_request('https', d, output_file,
                         html_output, allowed_http_responses, nmap_output, ip, output_directory)
            time.sleep(1)

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
        except subprocess.TimeoutExpired:
            pass
        else:
            pass


def enumerate_from_crt_sh(domain):
    '''
        Perform subdomains enumeration using crt.sh service
    '''
    base_url = "https://crt.sh/?q={}&output=json".format(domain)
    data = {}
    enumerated_subdomains = []

    resp = requests.get(base_url)

    if resp.status_code == 200:
        data = json.loads(resp.content.decode('utf-8'))
        for elem in data:
            if elem['common_name'] not in enumerated_subdomains:
                enumerated_subdomains.append(elem['common_name'])

        if len(enumerated_subdomains) > 0:
            print("{}[+] Done! Found {} subdomains, performing HTTP servers enumeration...{}".format(
                colors['cyan'], len(enumerated_subdomains), colors['white']))
            return enumerated_subdomains
    else:
        exit("[-] No data retrieved for domain {}".format(domain))


def main():
    parser = argparse.ArgumentParser()
    allowed_http_responses = []

    parser.add_argument(
        "-f", "--file", help="File with list of hostnames to check (-t/--target will be ignored)")
    parser.add_argument(
        "-t", "--target",
        help="Target domain - will use crt.sh to perform subdomain enumeration (-f/--file will be ignored)")
    parser.add_argument(
        "-s", "--success", help="Show all responses, including exceptions", action='store_true')
    parser.add_argument(
        "-o", "--output", help="Path to text output file with all domains with identified web servers")
    parser.add_argument(
        "-d", "--dir", help="Output directory name (default: report/)")
    parser.add_argument(
        "-c", "--code", help="Show only selected HTTP response status codes, comma separated",
        default='200,206,301,302,403,422,500'
    )
    parser.add_argument(
        "-n", "--nmap", help="use nmap for port scanning (slows down the whole enumeration A LOT, so be warned!)",
        action='store_true'
    )
    parser.add_argument(
        "-p", "--ports", help="--top-ports option for nmap (default = 100)", default=100
    )

    args = parser.parse_args()

    if args.nmap:
        nmap = True

    output_directory = _set_output_directory(args)

    if args.code:
        allowed_http_responses = args.code.split(',')
    else:
        allowed_http_responses = ['200', '301', '500']

    nmap_top_ports = args.ports

    # set options
    show = True if args.success else False

    # use provided file with list of hostnames or perform subdomain enumeration with crt.sh:
    if args.target is None and args.file is not None and os.path.isfile(args.file):
        domains = open(args.file, 'r').readlines()
    elif args.target is not None and args.file is None:
        domains = enumerate_from_crt_sh(args.target)
    else:
        exit('[-] No file with hostnames or domain to recon. Use either -f or -t option')

    # create dir for HTML report
    if os.path.isdir('reports') == False:
        os.mkdir('reports')
    if os.path.isdir('reports/{}'.format(output_directory)) == False:
        os.mkdir('reports/{}'.format(output_directory))

    # starts output HTML
    html_output = open(
        'reports/{}/__denumerator_report.html'.format(output_directory), 'w+')
    create_output_header(html_output)

    # if output filename was specified, create it and use to write report result
    if args.output:
        output_filename = os.path.join(
            'reports', output_directory, args.output)
        output_file = open(output_filename, 'w+')
    else:
        output_file = open('__enumerated_domains.txt', 'w+')

    # main loop
    enumerate_domains(domains, output_file, html_output,
                      allowed_http_responses, nmap_top_ports, output_directory, show)

    # finish HTML output
    create_output_footer(html_output)
    html_output.close()

    # close output file
    if args.output:
        output_file.close()

def _set_output_directory(args):
    if args.dir:
        output_directory = args.dir
    else:
        output_directory = DEFAULT_DIRECTORY
    return output_directory


if __name__ == "__main__":
    main()
