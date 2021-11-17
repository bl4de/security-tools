from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

'''
Vi.py - an automated script to extract all inteersting information from website

@author: bl4de <bl4de@wearehackerone.com>

@TBD:
- refactor scafolding code
- extract JavaScript files -> scan them for stuff 
  (API endpoints, secrets, hardcoded information etc.)
- parse HTML for stuff
- harvest useful information from any comment found (in HTML and JS alike)
- other? (TBA)

- add as a submodule (enabled by cmd option) to denumerator.py 
  and perform full recon of every website found in scope
'''

user_url = str(input('[+] Enter Target URL To Scan: '))
urls = deque([user_url])
MAX_COUNT = 10

scraped_urls = set()
emails = set()
javascript_files = set()

count = 0
try:
    while len(urls):
        count += 1
        if count == MAX_COUNT:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print('[%d] Processing %s' % (count, url))
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.IGNORECASE))
        emails.update(new_emails)

        new_javascripts = set(re.findall(
            r"[a-z0-9\.\-_]+\.js", response.text, re.IGNORECASE
        ))
        javascript_files.update(new_javascripts)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] Closing!')

for mail in emails:
    print(mail)
for js_file in javascript_files:
    print(js_file)
