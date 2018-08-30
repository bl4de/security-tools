#!/usr/bin/python
"""
Dictionary attack ZIP password cracker
https://github.com/igniteflow/violent-python/blob/master/pwd-crackers/zip-crack.py
"""
import zipfile
import argparse


def main(zipfilename, dictionary):
    """
    Zipfile password cracker using a brute-force dictionary attack
    """
    # zipfilename = 'secret.zip'
    # dictionary = '/Users/bl4de/hacking/dictionaries/passwords_2150000.txt'

    password = None
    zip_file = zipfile.ZipFile(zipfilename)
    with open(dictionary, 'r') as f:
        for line in f.readlines():
            password = line.strip('\n')
            # print password
            try:
                zip_file.extractall(pwd=password)
                password = 'Password found: %s' % password
            except:
                pass
    print password

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
