#!/usr/bin/env python
welcome = """
--- dENUMerator ---

by bl4de | bloorq@gmail.com | Twitter: @_bl4de | HackerOne: bl4de

Enumerates list of subdomains (output from tools like Sublist3r or subbrute)
and creates output file with servers responding on port 80/HTTP

This indicates (in most caes) working webserver

usage:
$ subdomain-http-enumerate.py [domain_list]
"""
import requests
import sys

HTTP_OK = 200


def usage():
    print welcome


def enumerate_domains(domains, output_file):
    i = len(domains)
    for d in domains:
        try:
            d = d.strip('\n')
            resp = requests.get('http://' + d,
                                timeout=5,
                                allow_redirects=False,
                                verify=False,
                                headers={
                                    'Host': d
                                })
            if resp.status_code == HTTP_OK:
                print '[+] domain {} HTTP OK'.format(d)
                output_file.write('{}\n'.format(d))

        except requests.exceptions.InvalidURL:
            print '[-] {} is not a valid URL :/'.format(d)
        except requests.exceptions.ConnectTimeout:
            print '[-] {} :('.format(d)
            continue
        except requests.exceptions.ConnectionError:
            print '[-] connection to {} aborted :/'.format(d)
        except requests.exceptions.ReadTimeout:
            print '[-] {} read timeout :/'.format(d)
        except requests.exceptions.TooManyRedirects:
            print '[-] {} probably went into redirects loop :('.format(d)
        else:
            pass


if (len(sys.argv) < 2):
    print welcome
    exit(0)

domains = open(sys.argv[1].strip(), 'rw').readlines()
output_file = open('output.txt', 'w')

enumerate_domains(domains, output_file)

output_file.close()
