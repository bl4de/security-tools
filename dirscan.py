#!/usr/bin/python
#
# webserver dir bruteforce scanner
#
import sys
import urllib


def main(__server, __port, __path, __wordlist):
    if len(__wordlist) > 0:
        _counter = 1
        _totalWordList = len(__wordlist)
        # 1/10 of progress indicator
        _step = int(_totalWordList / 10)

        print "\33[36m Start scan with %d known names.\n\33[0m" % _totalWordList

        # print _step
        for _directory in __wordlist:
            if _counter % _step == 0:
                print "\33[32m scanned %d of %d so far, continue...\33[0m" % ( _counter, len(__wordlist))

            _url = __server + ':' + __port + '/' + __path + '/' + _directory
            # print _url
            resp = urllib.urlopen(_url)
            # print resp.code
            if resp.code == 200:
                print '\n\33[33m' + _url + '\33[0m'

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

    main(server, port, path, wordlist)
