import sys
import os
import subprocess
import re

# Still working on my naming skills (Dont judge me) );


def main():
    def sanitize_string(dirty_string):
        return dirty_string.replace(r'\n', '').strip()

    # This one dirty way I can come up with to parse the text
    def _parse_ssid_string(ssid_str):
        first_parse = re.search(r'.*(?=Mode)', ssid_str)
        sec_parse = re.search(r'(?<=ESSID:).*', first_parse.group())
        return sanitize_string(sec_parse.group())

    def _check_current__ssid():
        try:
            ssid_class = subprocess.run("iwconfig", capture_output=True)
            ssid_str = str(ssid_class.stdout)
            return _parse_ssid_string(ssid_str)
        except IOError:
            raise Exception("Error checking wifi")

    def _find_wifi_pass(ssid):
        try:
            os.system("sudo cat /etc/NetworkManager/system-connections/" +
                      ssid + " | grep psk=")
        except IOError:
            raise Exception("Error reading file")

    if sys.platform.startswith("linux"):
        ssid = _check_current__ssid()
        if "off" not in ssid:
            _find_wifi_pass(ssid)
            print("Password for %s  is after psk above" % ssid)
        else:
            print("Not connected to wifi")
    else:
        print("Script support only linux systems")


if __name__ == "__main__":
    main()
