#! /usr/bin/env python

import os
import requests
import xml.etree.ElementTree as ET

class vars:
    version = "v2.0.0"
    p_switch = "switch2 | %s >> "
    p_choose = "choose item | >> "
    api_proto = "http://"
    api_ip = "192.168.54.75"
    api_res = "/addons/xmlapi/"

class cmds:
    list = ["list", "l"]
    help = ["help", "h"]
    quit = ["quit", "q"]
    clear = ["clear", "c"]
    back = ["back", "b"]

class subcmds:
    list = [ "rooms", "devices", "states", "programs" ]

class rtrn:
    err1 = "Unknown command\n"

def cmd_help():
    print("Version: %s" % vars.version)
    print("ToDo: Help")

def ccu_list(list):
    list_assignment = {
        "rooms": "roomlist.cgi",
        "devices": "devicelist.cgi",
        "states": "statelist.cgi",
        "programs": "programlist.cgi"
        }

    url = vars.api_proto + vars.api_ip + vars.api_res + list_assignment[list]
    r = requests.get(url, stream=True)

    root = ET.fromstring(r.text)

    for dev in root.findall('device'):
        dev_name = dev.attrib['name']
        print(dev_name)
        for ch in root.findall('device/channel'):
            ch_name = ch.attrib['name']
            print(ch_name)


def cmd_list():
    for v in subcmds.list:
        print(v)

    cmd = "read"
    while cmd not in cmds.back and cmd not in cmds.quit:
        cmd = input(vars.p_switch % "list")

        if cmd in subcmds.list:
            ccu_list(cmd)

        else:
            print(rtrn.err1)
            cmd_help()

def main():
    cmd = "read"

    os.system('clear')
    while cmd != "quit":

        cmd = input(vars.p_switch % "main")
        if cmd in cmds.list:
            cmd_list()

        elif cmd in cmds.help:
            cmd_help()

        elif cmd in cmds.clear:
            os.system('clear')

        elif cmd in cmds.quit:
            exit(0)

        elif cmd == "":
            pass

        else:
            print(rtrn.err1)
            cmd_help()


if __name__ == '__main__':
    main()
