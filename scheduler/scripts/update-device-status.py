#! /usr/bin/env python

import requests
import threading
import time
import sys

sys.path.append("/scheduler/bin")
from classes.const import const

def trigger_update():
    url = const.upd_proto + const.upd_addr + const.upd_res
    sys.stdout.write(str(url))
    r = requests.get(url)
    sys.stdout.write("ERROR: Status Code " + str(r.status_code))

def main():
    ticker = threading.Event()
    while not ticker.wait(const.upd_interval):
        trigger_update()


if __name__ == '__main__':
    main()
