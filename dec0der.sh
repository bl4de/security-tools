#!/bin/bash

# simple command line decoder/enmcoder
# by bl4de <bl4de@wearehackerone.com>
#
# invoke:
# dec0der [FROM] [string]

FROM=$1
STRING=$2

if [[ $FROM == 'ascii' ]]; then
    echo $STRING | xxd -r -p
fi

if [[ $FROM == 'base64' ]]; then
    echo $STRING | base64 -D
fi
