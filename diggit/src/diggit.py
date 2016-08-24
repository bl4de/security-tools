#!/usr/bin/python
#
# bl4de | <bloorq@gmail.com> | https://twitter.com/_bl4de
#
# diggit - gets .git repository
import argparse
import os
import re

# some common definitions
VERSION = "1.0.0"
OBJECT_DIR = "/.git/objects/"

Black = '\33[30m'
Red = '\33[31m'
Green = '\33[32m'
Yellow = '\33[33m'
Blue = '\33[34m'
Magenta = '\33[35m'
Cyan = '\33[36m'
White = '\33[37m'
_endline = '\33[0m'


def print_banner():
    """Prints credits :)"""
    print "\n\n", "#" * 78
    print "###", " " * 70, "###"
    print "###", " " * 70, "###"
    print "###         diggit.py  |  Twitter: @_bl4de  " \
          "| GitHub: bl4de                ###"
    print "###", " " * 70, "###"
    print "###", " " * 70, "###"
    print "#" * 78


def print_object_details(object_type, object_content, object_hash):
    """Prints object details"""
    print "\n" + Cyan + "#" * 12 + " " + object_hash \
          + " information " + "#" * 12 + _endline
    print "\n{0}[*] Object type: {3}{2}{1}{3}".format(Green, object_type, Red,
                                                      _endline)
    print "{0}[*] Object content:{1}\n".format(Green, _endline)
    print "{0}{1}{2}".format(Yellow, object_content, _endline)

    # print "\n" + Cyan + "#" * 78 + _endline


def get_object_url(object_hash):
    """Returns object git url"""
    return OBJECT_DIR + object_hash[0:2] + "/" + object_hash[2:]


def get_object_dir_prefix(object_hash):
    """Returns object directory prefix (first two chars of object hash)"""
    return object_hash[0:2] + "/"


def get_object_hash_from_object_desc(git_object_content):
    """returns object hash without control characters"""
    return git_object_content.split(" ")[1][:40]


def save_git_object(base_url, object_hash, be_recursive):
    """Saves git object in temporary .git directory preserves its path"""
    complete_url = base_url + "/" + get_object_url(object_hash)

    os.system("curl --silent '" + complete_url + "' --create-dirs -o '" +
              dummy_git_repository + get_object_url(object_hash) + "'")

    git_object_type = os.popen("cd " + dummy_git_repository + OBJECT_DIR +
                               get_object_dir_prefix(object_hash) +
                               " && git cat-file -t " + object_hash).read()

    git_object_content = os.popen("cd " + dummy_git_repository + OBJECT_DIR +
                                  get_object_dir_prefix(object_hash) +
                                  " && git cat-file -p " + object_hash).read()
    print_object_details(git_object_type, git_object_content, object_hash)

    # get actual tree from commit
    if git_object_type.strip() == "commit" and be_recursive is True:
        save_git_object(baseurl,
                        get_object_hash_from_object_desc(git_object_content),
                        be_recursive)

    if git_object_type.strip() == "tree" and be_recursive is True:
        for obj in git_object_content.split(" "):
            obj = obj[:40]
            if re.match(r"[a-zA-Z0-9]", obj):
                save_git_object(baseurl, obj, be_recursive)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            diggit.py - get information about Git object(s) from remote
                        repository
        """)
    parser.add_argument('-u', help='URL of remote Git repository location')
    parser.add_argument('-t',
                        help='path to temporary Git folder on local machine')
    parser.add_argument('-o', help='object hash (SHA-1, all 40 characters)')
    parser.add_argument('-r', default=False,
                        help='be recursive (if commit or tree hash '
                             'found, go get all blobs too). Default is \'False\'')

    args = parser.parse_args()

    # domain, base path for .git folder, eg. http://website.com
    baseurl = args.u

    # hash of object to save
    objecthash = args.o
    be_recursive = True if args.r else False

    # temporary dir with dummy .git structure (create it first!)
    dummy_git_repository = args.t

    if baseurl and objecthash:
        print_banner()
        save_git_object(args.u, args.o, be_recursive)
        print "\n" + Cyan + "#" * 78 + _endline
