#!/usr/bin/python
"""
compare.py

Creates snapshots and checksums of websites
Compares snapshots
Shows changes between snapshots
"""
import requests
import os

site_url = os.sys.argv[1]
snapshot_filename = site_url.replace('https://','').replace('http://','').replace('/','_').replace(':','_').replace('.','_') + '_SNAPSHOT'
differencies = 0

res = requests.get(site_url)

if os.path.isfile(snapshot_filename):
    print '\n[+] snapshot found, compare snapshot with current source...'
    snapshot_source = open(snapshot_filename, 'r').readlines()
    site_source = res.text.encode('utf-8').split('\n')
    line_counter = 0
    
    for snapshot_line in snapshot_source:
        # print 'snapshot:  ' + snapshot_line.strip()
        # print 'source:    ' + site_source[line_counter].strip()

        if snapshot_line.strip() != site_source[line_counter].strip():
            print '>>>>>     snaphsot line {}: '.format(line_counter + 1)
            print snapshot_line
            print '\n<<<<<     site source line {}'.format(line_counter + 1)
            print site_source[line_counter]

            print '\n--------------------------------------------------------------------------------------------------\n'
            differencies = differencies + 1

        line_counter = line_counter + 1

else:
    print '\n[+] snapshot not found, saving snapshot...'
    f = open(snapshot_filename, 'w')
    f.write(res.text.encode('utf-8'))

if differencies > 0:
    print '[+] {} differencies between snapshot and current source found'
else:
    print '[+] no differencies found; snapshot and current {} source are identical'.format(site_url)    
print '\n[+] DONE.'
