#! /usr/bin/env python

PAGE_TITLE = "tangogolf Switch 2"

SEND_FILE_MAX_AGE_DEFAULT = 0

LOGLEVEL = "INFO"

REDIS_URL = "redis://switch2-redis:6379/0"

HMIP_API_DEVICES = ["hmip-broll", "hmip-bwth", "hmip-wth-2", "hmip-psm", "hmip-fsm", "hmip-bsm"]
HMIP_API_TYPES = ["LEVEL", "SET_POINT_TEMPERATURE","STATE"]
HMIP_API_BASE_URL = "http://192.168.54.75/addons/xmlapi/"
HMIP_API_ROOMLIST = "roomlist.cgi"
HMIP_API_STATELIST = "statelist.cgi"
HMIP_API_FUNCTIONLIST = "functionlist.cgi"
HMIP_API_STATE = "state.cgi"

MHIP_MODEL_PO = ["hmip-psm", "hmip-fsm", "hmip-bsm"]
MHIP_MODEL_TH = ["hmip-wth-2", "hmip-bwth"]
MHIP_MODEL_RS = ["hmip-broll"]

NAVSTART_EXCEPTION = { '2180': 'po', '3517': 'th', '1215': 'th', '1214': 'po', '1223': 'po' }
