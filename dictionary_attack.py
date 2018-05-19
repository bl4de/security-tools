#!/usr/bin/python

import hashlib

wordlist = open('/Users/bl4de/hacking/dictionaries/rockyou.txt', 'r').readlines()
iterations = 1

for password in wordlist:
    if hashlib.sha1(password.strip()).hexdigest() == "6d9de275b50b7cfd1a98238182a39b61f1eb9a9a":
        print "[+] password found!!! -> {} after {} iterations".format(password.strip(), iterations)
        exit(0)
    iterations = iterations + 1

print "[-] password not found :("