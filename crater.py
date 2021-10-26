#!/usr/bin/env python3
import sys
import requests


domain = sys.argv[1]
base_url = "https://crt.sh/?q={}&output=json".format(domain)

resp = requests.get(base_url)

if resp.status_code == 200:
    print(resp.content)
    