"""
bl4de | bloorq@gmail.com | Twitter: @_bl4de | HackerOne: bl4de

This file contains all HTTP header payloads for headshot.py
"""


# HTTP methods
HTTP_METHODS = ['HEAD', 'GET', 'POST', 'OPTIONS', 'PUT', 'TRACE', 'DEBUG']

HTTP_HEADERS = ['User-Agent', 'Referer', 'X-Forwared-For',
                'X-Requested-With', 'Content-Type', 'Cookie']
# Headers payloads - put any payload you want to test here:
HEADERS_PAYLOADS = [
    'application/json',
    'application/xml',
    'text/html',
    'text/plain',
    'text/javascript',
    'image/jpeg',
    'image/png',
    'application/pdf',
    '',
    '"',
    'Fake',
    'Fake' * 20,
    'Mozilla',
    'javascript://\'/</title></style></textarea></script>--><p" %0D %0A onclick=alert()//>*/alert()/*',
    '%0d%0a',
    '%0d%0aTest test',
    '\\n',
    '\\n\\r',
    '\\n\\r test test',
    '',
    '"',
    'Fake',
    'http://fake',
    'http://google.ie',
    'https://google.ie',
    'ftp://server.com',
    'ssh://127.0.0.1',
    'ssh://root:toor@127.0.0.1',
    '--',
    '//',

]

BODY_CONTENT = [
    """

<?xml version="1.0"?>
<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
      <title>XML Developer's Guide</title>
      <genre>Computer</genre>
      <price>44.95</price>
      <publish_date>2000-10-01</publish_date>
      <description>An in-depth look at creating applications 
      with XML.</description>
   </book>
</catalog>


    """,

    """
    {date: 'today', user: 'admin'}
    """
]
