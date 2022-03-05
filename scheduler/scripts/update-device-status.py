#! /usr/bin/env python

import logging
import signal
import requests
import threading
import time
import sys

sys.path.append("/scheduler/bin")
from classes.const import const

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout,
                    format = log_format,
                    level = const.loglevel)
logger = logging.getLogger()


def terminate_process(signalNumber, frame):
    logger.info("Scheduler stopped with signal %s" % signalNumber )
    sys.exit()

def trigger_update():
    url = const.upd_proto + const.upd_addr + const.upd_res
    sys.stdout.write(str(url))
    r = requests.get(url)
    sys.stdout.write("ERROR: Status Code " + str(r.status_code))

def main():
    logger.info("Scheduler started")
    ticker = threading.Event()
    while not ticker.wait(const.upd_interval):
        trigger_update()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, terminate_process)
    main()
