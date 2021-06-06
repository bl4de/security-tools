#!/usr/bin/env python3
'''
    CODEStructor.py - Static Code Analysis grep-like tool on steroids :)
    - grep-like search for dangerous code patterns, sources and sinks
    - search for secrets, hardcoded credentials, interesting strings like hashes etc.
    - detailed, colorful output with configurable verbosity level
    - based on my previous tools: nodestructor and pef

    @author bl4de <bl4de@wearehackerone.com>
    @github https://github.com/bl4de/security-tools
'''
import argparse

