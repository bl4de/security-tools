#!/usr/bin/python
from console_output_beautifier import ConsoleOutputBeautifier

summary = {
    "comment": [],
    "script": [],
    "resources": [],
    "javascript": [],
    "debug": [],
    "admin": []
}


def print_banner():
    print ConsoleOutputBeautifier.getColor("green"), \
        "=" * 20, "HTML source code Analyzer", "=" * 20, "\n", \
        "  https://github.com/bl4de | https://twitter.com/_bl4de \n" \
        "  https://hackerone.com/bl4de | bloorq@gmail.com   ", \
        "\n\n", \
        ConsoleOutputBeautifier.getSpecialChar("endline")


def print_output_line(i, col, msg, msg_args, type="DEFAULT"):
    """printing line of output"""
    msg = "{} line {}: {} {}".format(
        ConsoleOutputBeautifier.getColor("white"),
        i,
        col,
        str(msg % msg_args)
    )
    print msg


def create_summary(_type, _message):
    """stores output line message in summary"""
    if _type.lower() in summary.keys() and _message != "":
        summary[_type].append(_message)


def show_stats(_file, i, _ident, _fw):
    """showing summary stats about HTML file"""
    print ConsoleOutputBeautifier.getColor(
        "green"), "\n------ SUMMARY -------\n"
    print "total lines of code:     %d" % (i)
    print "identified CMS:          %s" % (_ident)
    print "identified framework:    %s" % (
        _fw), ConsoleOutputBeautifier.getSpecialChar("endline")
    # end of summary
    print "\n"
