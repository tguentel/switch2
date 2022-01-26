#! /usr/bin/env python

PAGE_TITLE = "tangogolf Switch 2"

SEND_FILE_MAX_AGE_DEFAULT = 0

REDIS_URL = "redis://switch2-redis:6379/0"

HMIP_API_BASE_URL = "http://192.168.54.75:2121"
HMIP_API_DEVICE_URL = "/device"

HMIP_API_ALLOWED_DEVICES = [
        "hmip-broll",
        "hmip-bwth",
        "hmip-wth-2",
        "hmip-psm",
        "hmip-fsm",
        "hmip-swdo",
        "hmip-fci1",
        "hmip-srh"
        ]

HMIP_API_CONTROL_INDEX = {
        "hmip-broll": 4,
        "hmip-bwth": 1,
        "hmip-wth-2": 1,
        "hmip-psm": 3,
        "hmip-fsm": 2
        }

HMIP_API_CURRENT_INDEX = {
        "hmip-broll": 3,
        "hmip-bwth": 1,
        "hmip-wth-2": 1,
        "hmip-psm": 2,
        "hmip-fsm": 1,
        "hmip-swdo": 1,
        "hmip-fci1": 1,
        "hmip-srh":: 1
        }

HMIP_API_ALLOWED_TYPES = [
        "level",
        "set_point_temperature",
        "humidity",
        "actual_temperature"
        "state"
        ]



