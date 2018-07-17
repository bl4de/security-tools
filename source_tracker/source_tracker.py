#!/usr/bin/python
"""
source_tracker.py

@author: Rafal 'bl4de' Janicki

@Twitter: https://twitter.com/_bl4de
@HackerOne: https://hackerone.com/bl4de
@GitHub: https://github.com/bl4de

Website source changes tracker. When run for the first time against given url, creates snapshot file with current source.
Next run compares source from snapshot and shows all differencies between saved snapshot and current source.

Licence: MIT
"""
import requests
import os
import argparse

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
    "lightgrey": '\33[37m',
    "lightblue": '\33[94'
}


def create_filename_from_url(site_url):
    return site_url.replace('https://', '').replace(
        'http://', '').replace('/', '_').replace(':', '_').replace('.', '_') + '_SNAPSHOT'


def send_request(site_url):
    headers = {
        'Accept': 'text/html',
        'User-Agent': 'Some simple Python script'
    }
    return requests.get(site_url, headers=headers)


def abort(status_code):
    print '\n{}[-] response code: HTTP {}{}'.format(
        colors['red'], status_code, colors['white'])
    print '\n{}[-] ABORTING...{}\n'.format(colors['red'], colors['white'])
    exit(0)


def print_line(line, color):
    # TBD
    return

def print_diff(snapshot_source, site_source, line_counter):
    print '\n{}-- Change in line {} {}{}'.format(colors['red'],
                                       line_counter + 1, '-' * 80 + '\n', colors['white'])

    print '{}>>>>>  snaphsot line {}'.format(
        colors['yellow'], line_counter + 1)
    
    print '{}{}:\t{}{}'.format(colors['white'],line_counter, colors['grey'], snapshot_source[line_counter - 1].strip())
    print '{}{}:\t{}{}'.format(colors['white'],line_counter + 1, colors['cyan'], snapshot_source[line_counter].strip())
    print '{}{}:\t{}{}'.format(colors['white'],line_counter + 2, colors['grey'], snapshot_source[line_counter + 1].strip())
    
    print '\n{}<<<<<  site source line {}'.format(
        colors['yellow'], line_counter + 1)
    print '{}{}:\t{}{}'.format(colors['white'], line_counter, colors['grey'], site_source[line_counter - 1].strip())
    print '{}{}:\t{}{}'.format(colors['white'], line_counter + 1, colors['cyan'], site_source[line_counter].strip())
    print '{}{}:\t{}{}{}'.format(colors['white'], line_counter + 2, colors['grey'], site_source[line_counter + 1].strip(), colors['white'])


def main(site_url):
    snapshot_filename = create_filename_from_url(site_url)
    differencies = 0

    res = send_request(site_url)

    if res.status_code != 200:
        abort(res.status_code)

    if os.path.isfile(snapshot_filename):
        print '\n{}[+] snapshot found, compare snapshot with current source...{}'.format(
            colors['green'], colors['white'])
        snapshot_source = open(snapshot_filename, 'r').readlines()
        site_source = res.text.encode('utf-8').split('\n')
        line_counter = 0

        for snapshot_line in snapshot_source:
            if snapshot_line.strip() != site_source[line_counter].strip():
                print_diff(snapshot_source, site_source, line_counter)
                differencies = differencies + 1

            line_counter = line_counter + 1
        print '\n\n{}'.format('-' * 92)

    else:
        print '\n{}[+] snapshot not found, saving snapshot...{}'.format(
            colors['green'], colors['white'])
        f = open(snapshot_filename, 'w')
        f.write(res.text.encode('utf-8'))
        exit(0)

    if differencies > 0:
        print '{}[+] {} differencies between snapshot and current source found{}'.format(
            colors['green'], differencies, colors['white'])
    else:
        print '{}[+] no differencies found; snapshot and current {} source are identical{}'.format(
            colors['green'], site_url, colors['white'])

    print '\n{}[+] DONE.{}'.format(colors['green'], colors['white'])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url", help="An url to webiste/file (eg. https://hackerone.com or https://www.google-analytics.com/plugins/ua/ec.js)")

    args = parser.parse_args()
    site_url = args.url

    main(site_url)
