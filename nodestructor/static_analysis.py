#!/usr/bin/python
import re
import sys
import argparse

from imports.beautyConsole import beautyConsole

jsfile = open('/Users/bl4de/tmp/AppMeasurement.js', 'r')
file_read = jsfile.readlines()


# variables
variables = []
variable_to_trace = ''

variable_definition_regex = '(let|const|var)\s+([_$a-zA-Z0-9]+)'

line_no = 0


def decorate_varname(var_name):
    return beautyConsole.getColor("red") + var_name + beautyConsole.getColor("white")


def decorate_source(src_line):
    return beautyConsole.getColor("yellow") + src_line + beautyConsole.getColor("white")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--variable", help="Name of variable to trace")

ARGS = parser.parse_args()

if ARGS.variable:
    variable_to_trace = ARGS.variable.strip()

print "\n\n[+] STARTING ANALYSIS...\n"
for line in file_read:
    line = line.replace('\n', '')
    line_no = line_no + 1

    # print "line {}: {}".format(line_no, line)
    res = re.search(variable_definition_regex, line)
    if res:
        variable_name = res.group(2)
        if variable_name == variable_to_trace:
            print "\n[+] found {} variable definition in line {}:\n {}".format(decorate_varname(variable_name), line_no, decorate_source(line))
            inner_line_no = 0

            if variable_name == variable_to_trace:
                for inner_line in file_read:
                    inner_line = inner_line.replace('\n', '')
                    inner_line_no = inner_line_no + 1
                    if variable_name + '=' in inner_line.replace(' ', ''):
                        print "\n\t{} used in assignment in line {}:\n\t{}\n".format(decorate_varname(variable_name), inner_line_no, decorate_source(inner_line))
                    if '({})'.format(variable_name) in inner_line.replace(' ', ''):
                        print "\n\t{} used in function call as an argument in line {}:\n\t{}\n".format(decorate_varname(variable_name), inner_line_no, decorate_source(inner_line))

print "\n\n[+] DONE\n"
