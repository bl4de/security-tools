"""
bl4de | bloorq@gmail.com | Twitter: @_bl4de | HackerOne: bl4de

This file contains all HTTP header payloads for headshot.py
"""


# HTTP methods
HTTP_METHODS = ['HEAD', 'GET', 'POST', 'OPTIONS', 'PUT', 'TRACE', 'DEBUG']

# Headers payloads - put any payload you want to test here:
HEADERS_PAYLOADS = {
    'User-Agent': [
        '',
        '"',
        'Fake',
        'Fake' * 20,
        'Mozilla'
    ],
    'Referer': [
        '',
        '"',
        'Fake',
        'http://fake',
        'http://google.ie',
        'https://google.ie',
        'ftp://server.com',
        '--',
        '//'
    ]
}
