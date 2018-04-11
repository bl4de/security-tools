#!/usr/bin/python
import re

EXCLUDE = ['babel','xxx','eee']
subdir = 'node_modules/babel-register/lib'

print [e in subdir for e in EXCLUDE]