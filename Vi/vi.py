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
- refactor scafolding code [In progress]
- add argparser

- extract JavaScript files -> scan them for stuff 
  (API endpoints, secrets, hardcoded information etc.)
- parse HTML for stuff
- harvest useful information from any comment found (in HTML and JS alike)
- other? (TBA)

- add as a submodule (enabled by cmd option) to denumerator.py 
  and perform full recon of every website found in scope
'''


def extract_emails(emails: set, http_response: requests.Response) -> set:
    '''
        Extracts emails from provided HTTP response body and append them
        to already found set of emails
    '''
    emails.update(set(re.findall(
        r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", http_response.text, re.IGNORECASE)))
    return emails


def extract_javascript_files(javascript_files: set, http_response: requests.Response) -> set:
    '''
        Extracts JavaScript files urls from provided HTTP response body and append them
        to already found set of javascript_files
    '''
    javascript_files.update(set(re.findall(
        r"[a-z0-9\.\-_]+\.js", http_response.text, re.IGNORECASE
    )))
    return javascript_files


def parse_javascript_file(js_filename: str):
    '''
        Parse JavaScript file for interesting stuff    
    '''
    TYPE = 'DEBUG'
    print(f"[{TYPE}] parsing {js_filename} for interesting stuff...")
    pass


def tear_off():
    '''
        Performs data extraction stage
    '''
    for js_filename in javascript_files:
        parse_javascript_file(js_filename)

    pass


def recon(emails: set, javascript_files: set):
    '''
        Creates list of resources; some will be proceeded later in next 
        steps
    '''
    user_url = str(input('[+] Enter Target URL To Scan: '))
    urls = deque([user_url])
    MAX_COUNT = 2

    scraped_urls = set()

    count = 0

    try:
        '''
            main execution loop
        '''
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

            emails = extract_emails(emails, response)
            javascript_files = extract_javascript_files(
                javascript_files, response)

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
    for url in urls:
        print(url)
    for js_file in javascript_files:
        print(js_file)


if __name__ == "__main__":

    emails = set()
    javascript_files = set()

    # go through provided url; find emails, javascript files etc.
    recon(emails, javascript_files)

    # extract sensitive and interesting information from what was found
    tear_off()
