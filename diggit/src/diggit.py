#!/usr/bin/python
#
# bl4de | <bloorq@gmail.com> | https://twitter.com/_bl4de
#
# diggit - gets .git repository
import sys
import os

# some common definitions
VERSION = "0.0.1"
BASE_DIR = ".git/"
OBJECT_DIR = BASE_DIR + "objects/"

DESTINATION_FOLDER = "/Users/bl4de/hacking/playground/diggit/test1/"


def get_object_url(object_hash):
    return OBJECT_DIR + object_hash[0:2] + "/" + object_hash[2:]


def get_object_dir_prefix(object_hash):
    return object_hash[0:2] + "/"


def save_git_object(object_hash):
    complete_url = base_url + "/" + get_object_url(object_hash)

    os.system("curl '" + complete_url + "' --create-dirs -o '" +
              DESTINATION_FOLDER +
              get_object_url(object_hash) + "'")

    git_object_type = os.popen("cd " + DESTINATION_FOLDER + OBJECT_DIR +
                               get_object_dir_prefix(object_hash) +
                               " && git cat-file -t " + object_hash).read()

    print git_object_type


# main program
if __name__ == "__main__":
    print "### diggit.py ver. {v} ###".format(v=VERSION)

base_url = sys.argv[1]

save_git_object('07603070376d63d911f608120eb4b5489b507692')
