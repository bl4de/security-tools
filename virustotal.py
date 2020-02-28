#!/usr/bin/env python

from netaddr import *
import ctfpwn
import json
import time
import os
import argparse


virus_total_api_key = os.environ['VIRUS_TOTAL_API_KEY']


def process(cidr, logfile='virustotal.log'):
    total_found_domains = 0
    ips = IPSet([cidr])

    for ip in ips:
        print("\n[+] Resolving IP: {}".format(ip))
        found_domains = 0

        url = 'https://www.virustotal.com/vtapi/v2/ip-address/report?apikey={}&ip={}'.format(
            virus_total_api_key, str(ip))

        resp = ctfpwn.http_get(url)

        if resp:
            domains = json.loads(resp)

            if (domains['response_code'] == 0):
                print "[-] Empty response for {}".format(str(ip))
                time.sleep(15)
                continue

            f = open(logfile, 'a')

            for d in domains['resolutions']:
                print('>>> {}'.format(d['hostname']))
                found_domains = found_domains + 1
                f.write("{}\n".format(d['hostname']))

            print "[+] Found {} domain(s) on {}".format(found_domains, str(ip))
            print("[+] Waiting 15 sec. until next request (VirusTotal API restriction)")
            total_found_domains = total_found_domains + found_domains
            f.close()
        else:
            print "[-] Empty response for {}".format(str(ip))

        time.sleep(15)

    print("\n\n[+] Done, found {} in total".format(total_found_domains))


def main():

    parser = argparse.ArgumentParser()
    logfile = ''

    parser.add_argument(
        "-c", "--cidr", help="Network CIDR")
    parser.add_argument(
        "-o", "--output", help="Log filename (default - virustotal.log)")

    args = parser.parse_args()

    if args.output:
        logfile = args.output
    if args.cidr:
        process(args.cidr, logfile)


if __name__ == "__main__":
    main()
