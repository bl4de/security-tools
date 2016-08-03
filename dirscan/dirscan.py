#!/usr/bin/python
#
# webserver dir bruteforce scanner
#
import sys
import urllib


# TODO check protocol in __url
def scan_directory(__url, __directory):
    __full_url = __url + __directory
    resp = urllib.urlopen(__full_url)
    # DEBUG
    # print "scanning: {}".format(__url + __directory)
    if 199 < resp.code < 300:
        print '\33[32m HTTP {}: {} \33[0m'.format(resp.code, __full_url)
        return True
    if resp.code == 403:
        print '\33[33m HTTP {} Forbidden: {} \33[0m'.format(resp.code,
                                                            __full_url)
        return True
    if resp.code == 500:
        print '\33[31m HTTP {} Internal Server Error: {} \33[0m'.format(
            resp.code, __full_url)
        return True
    else:
        return False


def scan_file(__url):
    resp = urllib.urlopen(__url)
    # print resp.code
    if resp.code > 199 < 300:
        print '\33[32m HTTP {}: {} \33[0m'.format(resp.code, __url)
        return True
    if resp.code == 403:
        print '\33[33m HTTP {} Forbidden: {} \33[0m'.format(resp.code, __url)
    if resp.code == 500:
        print '\33[31m HTTP {} Internal Server Error: {} \33[0m'.format(
            resp.code, __url)
    else:
        return False


def scan_files(__url, __directory, __wordlist):
    # print _step
    for _filename in __wordlist:
        _url = __url + __directory + '/' + _filename + '.php'
        # _found = scan_file(_url)


def scan(__server, __wordlist):
    if len(__wordlist) > 0:
        _counter = 1
        _totalWordList = len(__wordlist)
        # 1/10 of progress indicator
        _step = int(_totalWordList / 10)
        if _step == 0:
            _step = 1

        print "\33[36m Start scan with {} known names.\n\33[0m".format(
            _totalWordList)

        # print _step
        for _directory in __wordlist:
            if _counter > 100 and _counter % _step == 0:
                print "\33[32m scanned {} of {} so far, continue...\33[0m" \
                    .format(_counter, len(__wordlist))
            _found = scan_directory(__server, _directory)
            if _found:
                # scan for files using the same wordlist
                scan_files(__server, _directory, __wordlist)

            _counter += 1

        print "\33[36m Done.\n\33[0m"


def run():
    # argv: dirscan server_url server_port base_dir [wordlist]
    if len(sys.argv) != 3:
        print "\nUsage:"
        print "\n./dirscan.py [SERVER_URL] [WORDLIST FILE]"
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
