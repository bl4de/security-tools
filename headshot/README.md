## headshot.py

headshot.py is HTTP headers fuzzer

The idea is to provide easy way to quickly enumerate multiple combinations of HTTP methods and headers to catch weird server behaviour.

This fragment contains definition of methods and headers and their values which ```headshot.py``` uses for fuzzing (TODO: change the way those values are provided; file with predefined ? )

```python

    # HTTP methods
    HTTP_METHODS = ['HEAD', 'GET', 'POST', 'OPTIONS', 'PUT', 'TRACE', 'DEBUG']

    # Headers payloads - put any payload you want to test here:
    HEADERS_PAYLOADS = {
        'User-Agent': [
            '', '"', 'Fake', 'Fake' * 20, 'Mozilla'
        ]
    }

```


### Usage

```
./headshot.py domain.com
```

Sample output:

```
bl4de:~/hacking/tools/bl4de/headshot $ ./headshot.py realpython.com
[+] Sending HEAD request:   received 200 OK with 24938 bytes of response
[+] Sending HEAD request:   received 200 OK with 24938 bytes of response
[+] Sending HEAD request:   received 200 OK with 24938 bytes of response
[+] Sending HEAD request:   received 200 OK with 24938 bytes of response
[+] Sending HEAD request:   received 200 OK with 24938 bytes of response
[+] Sending GET request:   received 200 OK with 24938 bytes of response
[+] Sending GET request:   received 200 OK with 24938 bytes of response
[+] Sending GET request:   received 200 OK with 24938 bytes of response
[+] Sending GET request:   received 200 OK with 24938 bytes of response
[+] Sending GET request:   received 200 OK with 24938 bytes of response
[+] Sending POST request:   received 200 OK with 24938 bytes of response
[+] Sending POST request:   received 200 OK with 24938 bytes of response
[+] Sending POST request:   received 200 OK with 24938 bytes of response
[+] Sending POST request:   received 200 OK with 24938 bytes of response
[+] Sending POST request:   received 200 OK with 24938 bytes of response
[+] Sending OPTIONS request:   received 200 OK with 0 bytes of response
[+] Sending OPTIONS request:   received 200 OK with 0 bytes of response
[+] Sending OPTIONS request:   received 200 OK with 0 bytes of response
[+] Sending OPTIONS request:   received 200 OK with 0 bytes of response
[+] Sending OPTIONS request:   received 200 OK with 0 bytes of response
[!] Sending PUT request:  response size is 231; HTTP respone status is: 405 Method Not Allowed
[!] Sending PUT request:  response size is 231; HTTP respone status is: 405 Method Not Allowed
[!] Sending PUT request:  response size is 231; HTTP respone status is: 405 Method Not Allowed
[!] Sending PUT request:  response size is 231; HTTP respone status is: 405 Method Not Allowed
[!] Sending PUT request:  response size is 231; HTTP respone status is: 405 Method Not Allowed
[!] Sending TRACE request:  response size is 223; HTTP respone status is: 405 Method Not Allowed
[!] Sending TRACE request:  response size is 223; HTTP respone status is: 405 Method Not Allowed
[!] Sending TRACE request:  response size is 223; HTTP respone status is: 405 Method Not Allowed
[!] Sending TRACE request:  response size is 223; HTTP respone status is: 405 Method Not Allowed
[!] Sending TRACE request:  response size is 223; HTTP respone status is: 405 Method Not Allowed
[!] Sending DEBUG request:  response size is 217; HTTP respone status is: 501 Method Not Implemented
[!] Sending DEBUG request:  response size is 217; HTTP respone status is: 501 Method Not Implemented
[!] Sending DEBUG request:  response size is 217; HTTP respone status is: 501 Method Not Implemented
[!] Sending DEBUG request:  response size is 217; HTTP respone status is: 501 Method Not Implemented
[!] Sending DEBUG request:  response size is 217; HTTP respone status is: 501 Method Not Implemented

[+] DONE
bl4de:~/hacking/tools/bl4de/headshot $
```

Each request and response is saved in ```headshot.log``` file.


### TODO

- handling redirects
- handling errors in general
- provide headers to test as argument (?)

