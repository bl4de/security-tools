#!/usr/bin/python
#
# webserver dir bruteforce scanner
#
import sys
import urllib


def scan_directory(__url, __directory):
    print __url + __directory
    resp = urllib.urlopen(__url + __directory)
    print resp.code
    if resp.code == 200:
        print '\33[33m' + __url + __directory + '\33[0m'
        return True
    else:
        return False


def scan_file(__url):
    resp = urllib.urlopen(__url)
    # print resp.code
    if resp.code == 200:
        print '\33[33m' + __url + '\33[0m'
        return True
    else:
        return False


def scan_files(__url, __directory, __wordlist):
    # print _step
    for _filename in __wordlist:
        _url = __url + __directory + '/' + _filename + '.php'
        _found = scan_file(_url)


def scan(__server, __port, __path, __wordlist):
    if len(__wordlist) > 0:
        _counter = 1
        _totalWordList = len(__wordlist)
        # 1/10 of progress indicator
        _step = int(_totalWordList / 10)
        if _step == 0:
            _step = 1

        print "\33[36m Start scan with %d known names.\n\33[0m" % _totalWordList

        # print _step
        for _directory in __wordlist:
            if _counter % _step == 0:
                print "\33[32m scanned %d of %d so far, continue...\33[0m" % ( _counter, len(__wordlist))

            _url = __server + ':' + __port + __path
            _found = scan_directory(_url, _directory)
            if _found:
                # scan for files using the same wordlist
                scan_files(_url, _directory, __wordlist)

            _counter += 1

        print "\33[36mDone.\n\33[0m"

# main program
if __name__ == "__main__":

    server = sys.argv[1]
    port = sys.argv[2]
    path = sys.argv[3]

    if len(sys.argv) > 4:
        wordlistFile = sys.argv[4]
        wordlistFileHandler = open(wordlistFile, 'r')

        wordlist = wordlistFileHandler.readlines()
    else:
        wordlist = []

    scan(server, port, path, wordlist)
