"""
Misc functions for headshot.py
"""
from modules.console_beautifier import ConsoleOutputBeautifier

def formatted_request(method, host, header, payload):
    return  """

    ---- REQUEST ----

    {} / HTTP/1.1
    Host: {}
    {}: {}

    ---- RESPONSE ----
    """.format(method, host, header, payload)


def line_start(fn):
    """
    line start decorator
    """
    def wrapper(*args, **kwargs):
        print "[+]"
        fn(*args, **kwargs)
    return wrapper


def response_description(method, resp_size, resp):
    message = "[+] Sending {} request:  {} received {} {} with {} bytes of response {}"

    if resp.status_code != 200:
        return "[-] {}Sending {} request:  response size is {}; HTTP respone status is: {} {}{}".format(ConsoleOutputBeautifier.getColor('red'), method, resp_size, resp.status_code, resp.reason, ConsoleOutputBeautifier.getColor('white'))
    else:
        return message.format(method,
                              ConsoleOutputBeautifier.getColor(
                                  'green'), resp.status_code,
                              resp.reason, resp.headers.get(
                                  'content-length'),
                              ConsoleOutputBeautifier.getColor('white'))

