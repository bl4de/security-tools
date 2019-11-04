#!/usr/bin/env python3

# JWT Decoder
import base64
import sys
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNDE2OTI5MDYxIiwianRpIjoiODAyMDU3ZmY5YjViNGViN2ZiYjg4NTZiNmViMmNjNWIiLCJzY29wZXMiOnsidXNlcnMiOnsiYWN0aW9ucyI6WyJyZWFkIiwiY3JlYXRlIl19LCJ1c2Vyc19hcHBfbWV0YWRhdGEiOnsiYWN0aW9ucyI6WyJyZWFkIiwiY3JlYXRlIl19fX0.gll8YBKPLq6ZLkCPLoghaBZG_ojFLREyLQYx0l2BG3E


def get_parts(jwt):
    return dict(zip(['header', 'payload', 'signature'], jwt.split('.')))


def decode_part(part):
    # use Base64URL decode plus optional padding.
    # === makes sure that padding will be always correct
    # extraneous padding is ignored
    return base64.urlsafe_b64decode(part + '===')


def encode_part(part):
    return base64.urlsafe_b64encode(part).decode('utf-8')


parts = get_parts(sys.argv[1])

header = decode_part(parts['header'])
print(header)

payload = decode_part(parts['payload'])
print(payload)
