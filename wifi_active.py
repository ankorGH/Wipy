import sys
import os
import subprocess
import re


# Still working on my naming (Dont judge me) );


def main():
    def sanitize_string(dirty_string):
        return dirty_string.replace(r'\n', '').strip()

    def _parse_ssid_string(ssid_str):
        re_ssid = re.compile(r"(?<=ESSID:).*(?=Mode)")
        matches = re_ssid.findall(ssid_str)
        ssid = ""
        for match in matches:
            ssid += sanitize_string(match)
        return ssid

    def _check_current__ssid():
        try:
            ssid_class = subprocess.run("iwconfig", capture_output=True)
        except IOError:
            raise Exception("Error checking wifi")

        ssid_str = str(ssid_class.stdout)
        return _parse_ssid_string(ssid_str)

    def _find_wifi_password(ssid):
        try:
            os.system("sudo cat /etc/NetworkManager/system-connections/" +
                      ssid + " | grep psk=")
        except IOError:
            raise Exception("Error reading file")

    if sys.platform.startswith("linux"):
        ssid = _check_current__ssid()
        if "off" not in ssid:
            _find_wifi_password(ssid)
            print("Password for %s  is text after psk= " % ssid)
        else:
            print("Not connected to wifi")
    else:
        print("Script support only linux systems")


if __name__ == "__main__":
    main()
