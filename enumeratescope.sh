#!/bin/bash
# Subdomain enumeration and web server discovery + screenshot tools
#
# @author: bl4de <bl4de@wearehackerone.com>
# @licence: MIT
#


## create domains/ folder
create_domains_folder() {
    if [ ! -d domains ]; then
        mkdir domains
        echo -e "$(date) domains/ folder created" >> subdomain_enum.log
    fi
}


## perform sublist3r and amass enumeration on each domain passed as an argument
enumerate_domain() {
    local DOMAIN=$1
    echo -e "$(date) started enumerate $DOMAIN" >> subdomain_enum.log
    sublister -d $DOMAIN -o domains/$DOMAIN.sublister
    amass enum -brute -min-for-recursive 1 -d $DOMAIN -o domains/$DOMAIN.amass
    
    if [ -s domains/$DOMAIN.sublister ] || [ -s domains/$DOMAIN.amass ]; then
        cat domains/$DOMAIN.* > domains/$DOMAIN.all
        sort -u -k 1 domains/$DOMAIN.all > domains/$DOMAIN
    fi
    rm -f domains/$DOMAIN.*
    echo -e "$(date) finished enumerate $DOMAIN, total number of unique domains found: $(cat domains/$DOMAIN|wc -l)" >> subdomain_enum.log
}

## processing all outputed list of domains into one, removing dups
## and sorting
create_list_of_domains() {
    echo -e "$(date) create final list of domains found..." >> subdomain_enum.log
    # concatenate and sort all domains from the target
    cat domains/*.* > domains/domains.all
    sort -u -k 1 domains/domains.all > domains/__domains
    # remove odd <BR> left by Sublist3r or amass :P
    sed 's/<BR>/#/g' domains/__domains | tr '#' '\n' > domains/__domains.final
    rm -f domains/domains.all
    echo -e "$(date) ... Done! $(cat domains/__domains.final|wc -l) unique domains gathered \o/" >> subdomain_enum.log
}


## runs denumerator
run_denumerator() {
    echo -e "$(date) denumerator started" >> subdomain_enum.log
    denumerator -f domains/__domains.final -c 200,302,403,500
    echo -e "$(date) denumerator finished" >> subdomain_enum.log
    echo -e "$(date) total webservers enumerated and saved to report: $(ls -l report/ | wc -l)" >> subdomain_enum.log
}


## performs nmap scan
run_virustotal_enum() {
    echo -e "$(date) virustotal $CIDR enumeration started" >> subdomain_enum.log
    # run virustotal.py reverse domain search
    virustotal --cidr $CIDR --output domains/virustotal.domains
    echo -e "$(date) virustotal $CIDR enumeration finished, $(cat domains/virustotal.domains|wc -l) domains found" >> subdomain_enum.log
}


## -----------------------------------------------------------------------------

# list of domains - text file, one domain in single line
DOMAINS=$1

# IP address range
CIDR=$2

echo -e "$(date) subdomain_enum.sh started" > subdomain_enum.log

# enusre that domains/ folder exists, if not create one
create_domains_folder

if [[ -n $CIDR ]]; then
    run_virustotal_enum
fi

cat $DOMAINS | while read DOMAIN
do
    enumerate_domain $DOMAIN
done

# concatenate and sort all domains from the target
create_list_of_domains
echo -e "\n[+} DONE. Found $(wc -l domains/__domains.final) unique subdomains"

# run denumerator on the domains/domains.final output file
run_denumerator

echo -e "\n[+} DONE."

## -----------------------------------------------------------------------------


