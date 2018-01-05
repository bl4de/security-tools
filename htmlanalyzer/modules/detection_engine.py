#!/usr/bin/python

"""HTML source analyzer
    bl4de | bloorq@gmail.com | Twitter: @_bl4de | H1: bl4de

    This tool goes through HTML document and shows all interesting places,
    like inline JavaScript calls, commented paths, 'debug' and similar
    words occurences, possible DOM Injection points, references to 
    resources like images or iframes

    detection_engine.py contains all specific logic which detects interesting
    parts of HTML
"""

import json
import re
from console_output_beautifier import ConsoleOutputBeautifier
from utils import print_output_line

# @TODO: libraries/framework detection
# detects frontend framework used

line_cache = []
vulners = json.loads(open('modules/vulners_api_rules.json').read())

def get_line(_line, _line_number, _chars=80):
    """returns formatted line to print"""
    return (_line_number, ConsoleOutputBeautifier.getColor("grey"), '\n\t\t'
            + _line.lstrip().rstrip()[0:_chars])


def detect_framework(_line):
    """frontend framework detection (simplified)
        WARNING!!!
        This detection is only some assumption based on some constant
        elements but can not be treat as 100% sure.
    """
    return detect_framework_vulners_db(_line)


def detect_framework_vulners_db(_line):
    for rule in vulners["data"]["rules"]:
        if re.match(vulners["data"]["rules"][rule]["regex"], _line):
            print vulners["data"]["rules"][rule]["alias"]
            return '{1} ({2})'.format(vulners["data"]["rules"][rule]["alias"], rule)

def identify(_line):
    """backend detection (simplified)"""
    _ident = "unknown"
    if "Joomla" in _line:
        _ident = "Joomla CMS"
    if "wp-content" in _line:
        _ident = "WordPress CMS"
    if 'content="Drupal"' in _line:
        _ident = "Drupal CMS"
    return _ident


def detect_developer_comments(_line, i):
    """detection of comments left by developers"""
    developer_comments = [
        'bug',
        'problem',
        'issue',
        'fix',
        'ticket',
        'bad',
        'todo',
        'inject',
        'crash',
        'trust',
        'dev',
        'temporary',
        'remove'
    ]

    for developer_comment in developer_comments:
        if developer_comment in _line.lower():
            print_output_line(i, ConsoleOutputBeautifier.getColor("yellow"),
                              "probably developer(s) related comment string found at line %d:  %s  %s",
                              get_line(_line, i, 120), "DOM BASED XSS")


def detect_dombased_xss(_line, i):
    """detection of DOM based XSS weaknesses"""
    dombased_calls = [
        'document.location',
        'document.url',
        'document.urlencoded',
        'document.referrer',
        'window.location',
        'document.write(',
        'document.writeln('
        '.innerHTML',
        'eval(',
        'setInterval(',
        'setTimeout(',
        'Function('
    ]

    for dombased_call in dombased_calls:
        if dombased_call in _line:
            print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                              "POSSIBLE DOM BASED INJECTION POINT found at line %d:  %s  %s",
                              get_line(_line, i, 120), "DOM BASED XSS")

def detect_ajax_calls(_line, i):
    ajax_calls = [
        '$.ajax',
        '$.getJSON',
        '$http.'
    ]

    for call in ajax_calls:
        if call in _line:
            print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                              "AJAX CALL (possible REST endpoint revealed) at line %d:  %s  %s",
                              get_line(_line, i, 120), "AJAX/REST CALL")


def detect_comments(_line, i):
    """detects comments"""
    if '<!--' in _line.lstrip():
        if "\"/" in _line:
            print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                              "COMMENTED PATH found at line %d: %s  %s",
                              get_line(_line, i, 120), "COMMENT")
        else:
            print_output_line(i, ConsoleOutputBeautifier.getColor("yellow"),
                              "COMMENT found at line %d: %s  %s",
                              get_line(_line, i, 120), "COMMENT")


def detect_admin_stuff(_line, i):
    """detects anything related to administration area"""
    if "admin" in _line.lower():
        print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                          "'admin' string found at line: %d: %s  %s",
                          get_line(_line, i, 120), "ADMIN")


def detect_debug(_line, i):
    """detects debug messages left by developers"""
    if "debug" in _line.lower():
        print_output_line(i, ConsoleOutputBeautifier.getColor("red"),
                          "DEBUG information found at line %d", i, "DEBUG")


def detect_external_resources(_line, i):
    """detects external resources like imgs, iframes, scripts"""
    if "src" in _line:
        if "<img" in _line:
            print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                              "PATH to external resource image "
                              " file found in %d: %s  %s",
                              get_line(_line, i, 120), "RESOURCES")
        if "<iframe" in _line:
            print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                              "IFRAME path found in %d:  %s  %s",
                              get_line(_line, i, 120), "RESOURCES")
        if "<script" in _line:
            print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                              "external SCRIPT path found in %d: %s  %s",
                              get_line(_line, i, 120), "RESOURCES")


def detect_javascript(_line, i):
    """detects inline JavaScript occurences, as a script or event handler
    inside HTML tag"""
    if "<script" in _line and "src" not in _line:
        print_output_line(i, ConsoleOutputBeautifier.getColor("green"),
                          "inline <SCRIPT> tag found at line %d", i, "SCRIPT")
    if "javascript:" in _line:
        print_output_line(i, ConsoleOutputBeautifier.getColor("cyan"),
                          "INLINE JavaScript event handler found at line %d", i,
                          "JAVASCRIPT")
