#!/bin/bash
# recon - basic recon of bugbounty target scope
# by bl4de | https://twitter.com/_bl4de

# params
SUBDOMAINS=$1
DICTIONARY=$2

mkdir out
OUTPUT_DIR=./out

echo
echo " usage: ./recon.sh [subdomains list] [dictionary file]"
echo
echo "  subdomains list - file with list of subdomains, if you have one"
echo "  dictionary file - optional; paht to dictionary used for files/dirs enumeration"
echo "                    dict.txt is used by default"
echo

if [ -z $2 ]
then
    # enter path to default dictionary for enumeration you want to use
    DICTIONARY=/Users/bl4de/hacking/tools/bl4de/recon/dict.txt
else
    DICTIONARY=$3
fi
echo "[+] using $DICTIONARY as dictionary file for files/dirs enumeration"

echo "[+] running recon.sh against $TARGET, please stand by..."
# # enumerate subdomains
# if [ -z $2 ]
# then
#     echo "[+] execute sublist3r $TARGET saving output to $TARGET_out file..."
#     sublist3r -d $TARGET > $TARGET"_out"
#     echo "[+] small sed-ing..."
#     cat $TARGET"_out" | sed  -e 's/\[92//;1,24d' > $TARGET"_subdomains"
#     SUBDOMAINS=$TARGET"_subdomains"
# else
#     echo "[+] using $2 as subdomains list"
#     SUBDOMAINS=$2
# fi

#  nmap 
echo "[+] scanning and directories/files discovery"
while read DOMAIN; do
    echo "[+] current target: $DOMAIN"
    nmap -sV -F $DOMAIN -oG $OUTPUT_DIR/$DOMAIN"_nmap" 1> /dev/null
    
    while read line; do
        if [[ $line == *"80/open/tcp//http"* ]]  
        then
            echo "[+] found webserver on $DOMAIN port 80/HTTP, running files/directories discovery..."
            wfuzz -f $OUTPUT_DIR/$DOMAIN"_wfuzz_80",raw --hc 404,301,302,401,000 -w $DICTIONARY http://$DOMAIN/FUZZ 1>/dev/null
        fi
        if [[ $line == *"443/open/tcp//http"* ]]
        then
            echo "[+] found webserver on $DOMAIN port 443/HTTPS, running files/directories discovery..."
            wfuzz -f $OUTPUT_DIR/$DOMAIN"_wfuzz_443",raw --hc 404,301,302,401,000 -w $DICTIONARY https://$DOMAIN/FUZZ 1>/dev/null
        fi
        if [[ $line == *"8080/open/tcp//http"* ]]
        then
            echo "[+] found webserver on $DOMAIN port 8080/HTTP, running files/directories discovery..."
            wfuzz -f $OUTPUT_DIR/$DOMAIN"_wfuzz_8080",raw --hc 404,301,302,401,000 -w $DICTIONARY http://$DOMAIN:8080/FUZZ 1>/dev/null
        fi
        if [[ $line == *"8008/open/tcp//http"* ]]
        then
            echo "[+] found webserver on $DOMAIN port 8008/HTTP, running files/directories discovery..."
            wfuzz -f $OUTPUT_DIR/$DOMAIN"_wfuzz_8008",raw --hc 404,301,302,401,000 -w $DICTIONARY http://$DOMAIN:8008/FUZZ 1>/dev/null
        fi
    done < $DOMAIN"_nmap"
done < $SUBDOMAINS

echo "[+] all done!!!"
echo
exit