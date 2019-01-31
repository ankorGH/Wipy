#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import re
import argparse
import logging

# Still working on my naming (Dont judge me) );


def sanitize_string(dirty_string):
    return dirty_string.replace(r'\n', '').strip().replace(r'"', '')


def parse_ssid_string(ssid_str):
    re_ssid = re.compile(r"(?<=ESSID:).*(?=Mode)")
    matches = re_ssid.findall(ssid_str)
    ssid = ""
    for match in matches:
        ssid += sanitize_string(match)
    return ssid


def check_current__ssid():
    try:
        ssid_class = subprocess.run("iwconfig", capture_output=True)
    except IOError:
        raise Exception("Error checking wifi")

    ssid_str = str(ssid_class.stdout)
    return parse_ssid_string(ssid_str)


def find_wifi_password(ssid):
    try:
        ssid_data = subprocess.run(
            ["sudo", "cat", f"/etc/NetworkManager/system-connections/{ssid}"], capture_output=True)
    except (IOError, FileExistsError):
        raise Exception("Error reading file")

    re_password = re.compile(r"(?<=psk=)[\w\d@!#$%^&*()]*")
    password = re_password.findall(str(ssid_data))
    return ''.join(password)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Wifi Checker",
        description="Check wifi password of your internet connection without leaving the terminal", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'current', help="Specify to check password of current wifi connection")
    return parser.parse_args()


def main():
    logging.basicConfig(format='%(message)s',
                        level=logging.DEBUG)
    args = parse_args()

    if args.current:
        if sys.platform.startswith("linux"):
            ssid = check_current__ssid()
            if "off" not in ssid:
                ssid_password = find_wifi_password(ssid)
                logging.info("Password for %s is %s" % (ssid, ssid_password))
            else:
                logging.info("Not connected to wifi")
        else:
            logging.info("Script support only linux systems")


if __name__ == "__main__":
    main()
