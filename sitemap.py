#! /usr/bin/env python
from bs4 import BeautifulSoup
import sys
import requests
import urlparse


def get_sitemap(url):
    get_url = requests.get(url)
    if get_url.status_code == 200:
        return get_url.text
    else:
        print('Unable to fetch sitemap: %s.' % url)


def process_sitemap(s):
    soup = BeautifulSoup(s, 'lxml')
    result = []

    for loc in soup.findAll('loc'):
        result.append(loc.text)

    return result


def is_sub_sitemap(url):
    parts = urlparse.urlparse(url)
    if parts.path.endswith('.xml') and 'sitemap' in parts.path:
        return True
    else:
        return False


def parse_sitemap(s):
    sitemap = process_sitemap(s)
    result = []

    while sitemap:
        candidate = sitemap.pop()

        if is_sub_sitemap(candidate):
            sub_sitemap = get_sitemap(candidate)
            for i in process_sitemap(sub_sitemap):
                sitemap.append(i)
        else:
            result.append(candidate)

    return result


def main():
    sitemap = get_sitemap(sys.argv[1])

    url_count = 0
    for url in parse_sitemap(sitemap):
        url_count += 1
        print("%5d) %s" % (url_count, url))
    print("-end-of-list-")


if __name__ == '__main__':
    main()
