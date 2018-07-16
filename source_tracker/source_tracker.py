#!/usr/bin/python
"""
compare.py

Creates snapshots and checksums of websites
Compares snapshots
Shows changes between snapshots
"""
import requests
import os


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
    print '\n[-] response code: HTTP {}'.format(status_code)
    print '\n[-] ABORTING...\n'
    exit(0)


def print_diff(snapshot_line, site_source, line_counter):
    print '\n-- LINE {} '.format(line_counter + 1) + '-' * 80 + '\n'
    print '>>>>>  snaphsot line {}\n: '.format(line_counter + 1)
    print snapshot_line
    print '\n<<<<<  site source line {}\n'.format(line_counter + 1)
    print site_source[line_counter]


site_url = os.sys.argv[1]
snapshot_filename = create_filename_from_url(site_url)
differencies = 0

res = send_request(site_url)

if res.status_code != 200:
    abort(res.status_code)

if os.path.isfile(snapshot_filename):
    print '\n[+] snapshot found, compare snapshot with current source...'
    snapshot_source = open(snapshot_filename, 'r').readlines()
    site_source = res.text.encode('utf-8').split('\n')
    line_counter = 0

    for snapshot_line in snapshot_source:
        if snapshot_line.strip() != site_source[line_counter].strip():
            print_diff(snapshot_line, site_source, line_counter)
            differencies = differencies + 1

        line_counter = line_counter + 1
    print '\n\n{}'.format('-' * 92)

else:
    print '\n[+] snapshot not found, saving snapshot...'
    f = open(snapshot_filename, 'w')
    f.write(res.text.encode('utf-8'))
    exit(0)

if differencies > 0:
    print '[+] {} differencies between snapshot and current source found'.format(
        differencies)
else:
    print '[+] no differencies found; snapshot and current {} source are identical'.format(
        site_url)
print '\n[+] DONE.'
