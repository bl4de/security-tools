#!/usr/bin/env python3

# JWT Decoder
import base64
import sys
import hmac
import hashlib
import binascii

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNDE2OTI5MDYxIiwianRpIjoiODAyMDU3ZmY5YjViNGViN2ZiYjg4NTZiNmViMmNjNWIiLCJzY29wZXMiOnsidXNlcnMiOnsiYWN0aW9ucyI6WyJyZWFkIiwiY3JlYXRlIl19LCJ1c2Vyc19hcHBfbWV0YWRhdGEiOnsiYWN0aW9ucyI6WyJyZWFkIiwiY3JlYXRlIl19fX0.gll8YBKPLq6ZLkCPLoghaBZG_ojFLREyLQYx0l2BG3E

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNDE2OTI5MDYxIiwianRpIjoiODAyMDU3ZmY5YjViNGViN2ZiYjg4NTZiNmViMmNjNWIiLCJzY29wZXMiOnsidXNlcnMiOnsiYWN0aW9ucyI6WyJyZWFkIiwiY3JlYXRlIl19LCJ1c2Vyc19hcHBfbWV0YWRhdGEiOnsiYWN0aW9ucyI6WyJyZWFkIiwiY3JlYXRlIl19fX0.15308fa263baaa57c2c84528d913ab75892352d927ccbd29e5af8fd783257996


def get_parts(jwt):
    return dict(zip(['header', 'payload', 'signature'], jwt.split('.')))


def decode_part(part):
    # use Base64URL decode plus optional padding.
    # === makes sure that padding will be always correct
    # extraneous padding is ignored
    return base64.urlsafe_b64decode(part + '===')


def encode_part(part):
    return base64.urlsafe_b64encode(part).decode('utf-8').replace('=', '')


def build_jwt(header, payload, key, alg='hmac'):
    message = f'{encode_part(header)}.{encode_part(payload)}'.encode()
    if alg == 'hmac':
        signature = hmac.new(key.encode(), message,
                             hashlib.sha256).hexdigest()
    elif alg == 'none':
        # if alg is set to 'none'
        signature = ''
    else:
        pass
    return f'{message}.{signature}'


parts = get_parts(sys.argv[1])

header = decode_part(parts['header'])
print(header)

payload = decode_part(parts['payload'])
print(payload)


jwt = build_jwt(header, payload, 'secrety')
print(jwt)
