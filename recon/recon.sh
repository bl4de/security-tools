#!/bin/bash
# r3c0n.sh by bl4de | twitter.com/bl4de

TARGET=$1
OUTPUT_FILE="$TARGET".log

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
LGRAY='\033[0;37m'

NC='\033[0m' # No Color

echo -e "${BLUE}[+]${NC} ${GREEN}nmap scanning...${NC}"
nmap -p- -A -sV $TARGET -o $OUTPUT_FILE 

echo -e "${BLUE}[+]${NC}  ${GREEN}nikto scanning...${NC}"
/Users/bl4de/hacking/tools/nikto/program/nikto.pl -host $TARGET >> $OUTPUT_FILE 

echo -e "${BLUE}[+]${NC}  ${GREEN}theHarvester scanning...${NC}"
theharvester -d $TARGET -b all >> $OUTPUT_FILE 

echo -e "${BLUE}[+]${NC}  ${GREEN}tryin to obtain domains for this IP...${NC}"
curl -L https://reverse.report/commonapi/v1/ip/$TARGET.json >> $OUTPUT_FILE
