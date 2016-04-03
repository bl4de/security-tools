#!/usr/bin/python
#
# bl4de | <bloorq@gmail.com> | https://twitter.com/_bl4de
#
# diggit - gets .git repository
import os
import sys

# some common definitions
VERSION = "0.0.1"
OBJECT_DIR = ".git/objects/"

Black = '\33[30m'
Red = '\33[31m'
Green = '\33[32m'
Yellow = '\33[33m'
Blue = '\33[34m'
Magenta = '\33[35m'
Cyan = '\33[36m'
White = '\33[37m'
_endline = '\33[0m'


def print_credits():
    print "#" * 68
    print "###    diggit.py  |  Twitter: @_bl4de  | GitHub: bl4de           ###"
    print "#" * 68


def print_usage():
    print "\n\nusage: ./diggit.py [url] [git_object_hash] [temporary_dir]\n"
    print " [url]               - url of web page with revealed .git directory"
    print " [git_object_hash]   - SHA1 of Git object, as found in .git/logs/head or similar"
    print " [temporary_dir]     - local directory with dummy Git folder structure"
    print "  (see https://github.com/bl4de/research/blob/master/hidden_directories_leaks/README.md#git for more information)"


def print_object_details(object_type, object_content):
    print "\n" + Cyan + "#" * 12 + " " + object_hash \
          + " information " + "#" * 12 + _endline
    print "\n{0}[*] Object type: {3}{2}{1}{3}".format(Green, object_type, Red,
                                                      _endline)
    print "{0}[*] Object content:{1}\n".format(Green, _endline)
    print "{0}{1}{2}".format(Yellow, object_content, _endline)

    print "\n" + Cyan + "#" * 78 + _endline


def get_object_url():
    return OBJECT_DIR + object_hash[0:2] + "/" + object_hash[2:]


def get_object_dir_prefix():
    return object_hash[0:2] + "/"


def save_git_object():
    complete_url = base_url + "/" + get_object_url()

    os.system("curl --silent '" + complete_url + "' --create-dirs -o '" +
              dummy_git_repository + get_object_url() + "'")

    git_object_type = os.popen("cd " + dummy_git_repository + OBJECT_DIR +
                               get_object_dir_prefix() +
                               " && git cat-file -t " + object_hash).read()

    git_object_content = os.popen("cd " + dummy_git_repository + OBJECT_DIR +
                                  get_object_dir_prefix() +
                                  " && git cat-file -p " + object_hash).read()
    print_object_details(git_object_type, git_object_content)


# main program
if __name__ == "__main__":

    if len(sys.argv) != 4:
        print_usage()
        exit(0)

    # domain, base path for .git folder, eg. http://website.com
    base_url = sys.argv[1]

    # hash of object to save
    object_hash = sys.argv[2]

    # temporary dir with dummy .git structure (create it first!)
    dummy_git_repository = sys.argv[3]

    if base_url and object_hash:
        save_git_object()
