#!/usr/bin/python
#
# Python script skeleton
#
import sys

_codes = {
    "<" : "&lt;",
    ">" : "&gt;",
    "/" : "&#47;",
    "'" : "&#39;",
    "\"" : "&quot;"
}

# encode special characters in HTML string into
# HTML escapes chars
def _encode(_str):
    print "before: ", _str
    for _toReplace in _codes.keys():
        _str = _str.replace(_toReplace, _codes[_toReplace])
        
    print "after: ", _str 
    

# main program
if __name__ == "__main__":
    str = sys.argv[1]
    
    # pass HTML string as an argument
    _encode(str)