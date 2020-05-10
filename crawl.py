#!/usr/bin/python
import sys
import json
import requests
import argparse
from bs4 import BeautifulSoup


def results(file):
    content = open(file, 'r').readlines() 
    for line in content:
        data = json.loads(line.strip()) 
    urls = []
    for url in data['results']:
        urls.append(url['url'])
    return urls


def crawl(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml') 
    links = soup.findAll('a', href=True) 
    for link in links:
        link = link['href']
        if link and link != '#':
            print '[+] {} : {}'.format(url, link)

if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument("file", help="ffuf results") 
    args = parser.parse_args() 
    urls = results(args.file)
    
    for url in urls:
        crawl(url)
