#!/usr/bin/python
#
# webserver dir bruteforce scanner
#
import sys
import urllib


# TODO check protocol in __url
def scan_directory(__url, __directory):

    resp = urllib.urlopen("http://" + __url + __directory)
    if resp.code == 200:
        print '\33[33m [{}] Found directory: {}\33[0m' \
            .format(resp.code, __url + __directory)
        return True
    else:
        return False


def scan_file(__url):
    resp = urllib.urlopen(__url)
    # print resp.code
    if resp.code == 200:
        print '\33[33m {} \33[0m'.format(__url)
        return True
    else:
        return False


def scan_files(__url, __directory, __wordlist):
    # print _step
    for _filename in __wordlist:
        _url = __url + __directory + '/' + _filename + '.php'
        # _found = scan_file(_url)


def scan(__server, __port, __path, __wordlist):
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

            if __path == "/":
                __path = ""

            _url = __server + ':' + __port + "/" + __path
            _found = scan_directory(_url, _directory)
            if _found:
                # scan for files using the same wordlist
                scan_files(_url, _directory, __wordlist)

            _counter += 1

        print "\33[36mDone.\n\33[0m"


def run():
    # argv: dirscan server_url server_port base_dir [wordlist]
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print "\nUsage:"
        print "\n./dirscan.py SERVER_URL PORT BASE_PATH [WORDLIST FILE]"
        exit(0)
    else:
        return


# main program
if __name__ == "__main__":

    run()

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
