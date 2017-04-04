#!/usr/bin/env python

"""
Automate tasks for full recon the target
Executed step(s) and used tools:

1. Enumerate subdomain(s) [sublist3r, https://github.com/aboul3la/Sublist3r]
2. find working HTTP servers in output list from Step 1. [denumerator, https://github.com/bl4de/security-tools/blob/master/denumerator/denumerator.py]

"""

import sys
import subprocess
import re


DOMAIN = ""
OUTPUT = open("OUTPUT", "rw")
HTML_OUTPUT_FILE = open("output.html", "w+")
HTML = open("template.html", "rw+").read()


################################  TESTS  #################################

def sublist3r_test(__args=[]):
    task_name = 'sublist3r'
    html_fragment = ""
    try:
        for subdomain in OUTPUT.readlines():
            html_fragment = html_fragment + \
                "<li>{}</li>".format(subdomain.strip())
        interpolate_html_fragment(task_name, html_fragment)
    except Exception, e:
        print "[-] Excpetion raised: {}".format(str(e))
        print "[-] sublist3r: missing domain name"
        exit(0)

###################################  TASKS  ##############################


def denumerator(__args=[]):
    """
    runs denumerator.py
    """
    task_name = 'denumerator'
    html_fragment = ""
    try:
        current_process = subprocess.Popen(
            ['denumerator', 'OUTPUT'])
        exit_code = current_process.wait()
        if exit_code == 0:
            for subdomain in open("output.txt").readlines():
                subdomain = subdomain.strip()
                html_fragment = html_fragment + \
                    '<li>HTTP server found on  <a href="http://{}" target="_blank"><b>{}</b></a></li>'.format(
                        subdomain, subdomain, subdomain)

        interpolate_html_fragment(task_name, html_fragment)
    except Exception, e:
        print "[-] Excpetion raised: {}".format(str(e))
        print "[-] denumerator: an error occured; denumerator failed; aborting"
        exit(0)


def sublist3r(__args=[]):
    """
    runs sublist3r
    """
    task_name = 'sublist3r'
    html_fragment = ""
    try:
        current_process = subprocess.Popen(
            ['sublist3r', '--domain', DOMAIN, '--output', 'OUTPUT'])
        exit_code = current_process.wait()
        if exit_code == 0:
            for subdomain in OUTPUT.readlines():
                html_fragment = html_fragment + \
                    "<li>{}</li>".format(subdomain.strip())

        interpolate_html_fragment(task_name, html_fragment)

    except Exception, e:
        print "[-] Excpetion raised: {}".format(str(e))
        print "[-] sublist3r: missing domain name"
        exit(0)


###############################  HELPERS  ################################


def interpolate_html_fragment(identifier, html_fragment):
    global HTML
    HTML = HTML.replace("#{}_output#".format(identifier), html_fragment)


def save_html_output(html_file, html_output):
    global DOMAIN
    html_output = re.sub(r'#DOMAIN#', DOMAIN, html_output, flags=re.MULTILINE)
    html_file.write(html_output)
    html_file.close()


def print_banner():
    """
    prints welcome banner
    """
    print "#####  Sword | by bl4de  #####\n\n"


def print_usage():
    """
    prints usage
    """
    print "usage: ./sword.py [domain] [steps] [exclude_tool(s)]\n\n"


def run(__task, __args):
    """
    task runner
    """
    try:
        __task(__args)
    except Exception, e:
        print "[-] Excpetion raised: {}".format(str(e))
        print "[-] something went wrong :("
        exit(0)

##########################################################################

# main program
if __name__ == "__main__":
    try:
        if sys.argv[1]:
            DOMAIN = sys.argv[1]

        print "[+] starting with {}".format(DOMAIN)

        # subdomain(s) enumeration
        run(sublist3r, [DOMAIN])
        # find working HTTP servers
        run(denumerator, [])

        print HTML

        # save HTML output to a file
        print "[+] saving HTML to a file"
        save_html_output(HTML_OUTPUT_FILE, HTML)

        print "[+] done\n\n\n"

    except Exception, e:
        print "[-] Excpetion raised: {}".format(str(e))
        exit(0)
