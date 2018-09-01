#!/usr/bin/python
"""
Dictionary attack ZIP password cracker
https://github.com/igniteflow/violent-python/blob/master/pwd-crackers/zip-crack.py
"""
import zipfile
import argparse


def main(zipfilename, dictionary):
    counter = 0
    """
    Zipfile password cracker using a brute-force dictionary attack
    """
    password = None
    zip_file = zipfile.ZipFile(zipfilename)
    passwords = open(dictionary, 'r').readlines()
    for p in passwords:
        password = p.strip('\n')
        counter = counter + 1
        if counter % 10000 == 0:
            print "[+] {} password checked so far...".format(counter)
        try:
            zip_file.extractall(pwd=password)
            print 'Password found: %s' % password
        except:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("zipfilename", help="Specify a .zip file to crack")
    parser.add_argument(
        "-w", "--wordlist", help="dictionary file")

    args = parser.parse_args()
    try:
        main(args.zipfilename, args.wordlist)
    except:
        print "[-] arguments error :("
