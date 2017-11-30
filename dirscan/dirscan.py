#!/usr/bin/python
#
# webserver dir bruteforce scanner
#
from __future__ import print_function
import sys
import urllib


# TODO check protocol in __url
def scan_directory(__url, __directory):
    url = (__url + __directory).strip()
    resp = urllib.urlopen(url)
    # DEBUG
    # print "scanning: {}".format(__url + __directory)
    if 199 < resp.code < 300:
        print('\33[32m [*] HTTP {}: {}'.format(resp.code, url))
        return True
    if resp.code == 403:
        print('\33[33m [*] HTTP {} Forbidden: {}'.format(resp.code,
                                                            url))
        return True
    if resp.code == 500:
        print('\33[31m [*] HTTP {} Internal Server Error: {}'.format(
            resp.code, url))
        return True
    else:
        return False


def scan_file(url):
    resp = urllib.urlopen(url.strip())
    # print resp.code
    if resp.code > 199 < 300:
        print('\33[32m [*] HTTP {}: {}'.format(resp.code, url))
        return True
    if resp.code == 403:
        print('\33[33m [*] HTTP {} Forbidden: {}'.format(resp.code, url))
    if resp.code == 500:
        print('\33[31m [*] HTTP {} Internal Server Error: {}'.format(
            resp.code, url))
    else:
        return False


def scan_files(url, directory, wordlist):
    # print _step
    for filename in wordlist:
        url = url + directory + '/' + filename + '.php'
        # _found = scan_file(_url)


def scan(server, wordlist):
    if len(wordlist) > 0:
        counter = 1
        totalWordList = len(wordlist)
        step = totalWordList / 10

        print("\33[36m [+] Start scan with {} known names".format(
            totalWordList))

        # print _step
        for directory in wordlist:
            found = scan_directory(server, directory)
            if found:
                # scan for files using the same wordlist
                scan_files(server, directory, wordlist)

            counter += 1
        print("\33[36m [+] Done.\n")


def run():
    # argv: dirscan server_url server_port base_dir [wordlist]
    if len(sys.argv) != 3:
        print("\nUsage:")
        print("\n./dirscan.py [SERVER_URL] [WORDLIST FILE]")
        exit(0)
    else:
        return


# main program
if __name__ == "__main__":

    run()

    server = sys.argv[1]

    if len(sys.argv) == 3:
        wordlist = open(sys.argv[2], 'r').readlines()
    else:
        wordlist = []
    scan(server, wordlist)
