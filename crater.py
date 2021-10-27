#!/usr/bin/env python3
import sys
import requests
import json

domain = sys.argv[1]
base_url = "https://crt.sh/?q={}&output=json".format(domain)
data = {}
extracted_domains = []

resp = requests.get(base_url)

if resp.status_code == 200:
    data = json.loads(resp.content.decode('utf-8'))
    for elem in data:
        if elem['name_value'] not in extracted_domains:
            extracted_domains.append(elem['name_value'])

    print(extracted_domains)
else:
    print("[-] No data retrieved for domain {}".format(domain))
