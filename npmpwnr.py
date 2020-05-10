#!/usr/bin/env python3
import requests
import json
import subprocess
import os
import re
import sys


limit = 10
skip = 100

registry_base_url = "https://registry.npmjs.com"
logfile = "vulnerable.log"

headers = {
    "User-Agent": "bl4de@wearehackerone"
}
npm_home_dir = "{}/node_modules".format(os.environ['HOME'])

patterns = [
    ".*url.parse\(",
    ".*[pP]ath.normalize\(",
    ".*fs.*File.*\(",
    ".*fs.*Read.*\(",
    ".*pipe\(res",
    ".*bodyParser\(",
    ".*eval\(",
    ".*exec\(",
    ".*execSync\(",
    ".*res.write\(",
    ".*child_process",
    ".*child_process.exec\(",
    ".*\sFunction\(",
    ".*execFile\(",
    ".*spawn\(",
    ".*fork\(",
    ".*setImmediate\(",
    ".*newBuffer\(",
    ".*\.constructor\("
]


def get_list_of_packages_to_process(keyword, size):
    res = requests.get(
        url="{}{}".format(
            registry_base_url, "/-/v1/search?text={}&size={}".format(keyword, size)),
        headers=headers
    )
    if res.status_code == 200:
        return res.json()

    return False


def get_package_details(pkg_name):
    res = requests.get(
        url="{}{}".format(registry_base_url, pkg_name),
            headers=headers
    )
    if res.status_code == 200:
        return res.json()

    return False


def install_package(pkg_name):
    subprocess.run(["npm", "i", pkg_name])


def process_files(subdirectory, sd_files, log):
    """
    recursively iterates ofer all files and checks those which meet
    criteria set by options only
    """
    for __file in sd_files:
        current_filename = os.path.join(subdirectory, __file)
        if current_filename[-3:] == '.js':
            perform_code_analysis(current_filename, log)


def perform_code_analysis(src, log):
    """
    performs code analysis, line by line
    """
    print_filename = True

    _file = open(src, "r")
    _code = _file.readlines()
    i = 0
    found = False
    for _line in _code:
        i += 1
        __line = _line.strip()
        for __pattern in patterns:
            __rex = re.compile(__pattern)
            if __rex.match(__line.replace(' ', '')):
                found = True
    if found == True:
        print("file {} is vulnerable".format(src))
        log.write("{}\n".format(src))


if len(sys.argv) < 2:
    exit('No keywork provided, exiting...')
else:
    keyword = sys.argv[1]

size = 10  # default
if len(sys.argv) == 3:
    size = int(sys.argv[2])

log = open(logfile, "w")

# get list of packages to process
pkgs = get_list_of_packages_to_process(keyword, size)

for pkg in pkgs['objects']:
    pkg_name = pkg['package']['name']
    install_package(pkg_name)
    log.write("\n{}\n".format(pkg_name))

    for subdir, dirs, files in os.walk("{}/{}".format(npm_home_dir, pkg_name)):
        process_files(subdir, files, log)
