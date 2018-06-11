#!/usr/bin/python
import re

jsfile = open('js/foobar.js', 'r')
file_read = jsfile.readlines()


# variables
variables = []

variable_definition_regex = '(let|const|var)\s+([_$a-zA-Z0-9]+)'

line_no = 0

print "\n\n[+] STARTING ANALYSIS...\n"
for line in file_read:
    line = line.replace('\n', '')
    line_no = line_no + 1

    # print "line {}: {}".format(line_no, line)
    res = re.search(variable_definition_regex, line)
    if res:
        variable_name = res.group(2)
        print "\n[+] found {} variable definition in line {}: {}".format(variable_name, line_no, line)
        inner_line_no = 0

        for inner_line in file_read:
            inner_line = inner_line.replace('\n', '')
            inner_line_no = inner_line_no + 1
            if variable_name in inner_line:
                print "   {} used in expression in line {}: {}".format(variable_name, inner_line_no, inner_line)

print "\n\n[+] DONE\n"