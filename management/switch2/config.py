#! /usr/bin/env python

PAGE_TITLE = "tangogolf Switch 2"

SEND_FILE_MAX_AGE_DEFAULT = 0

REDIS_URL = "redis://switch2-redis:6379/0"

HMIP_API_DEVICES = ["HmIP-BROLL", "HmIP-BWTH"]
HMIP_API_TYPES = ['LEVEL', 'SET_POINT_TEMPERATURE']
HMIP_API_BASE_URL = "http://192.168.54.75/addons/xmlapi/"
HMIP_API_ROOMLIST = "roomlist.cgi"
HMIP_API_STATELIST = "statelist.cgi"
HMIP_API_FUNCTIONLIST = "functionlist.cgi"
HMIP_API_STATE = "state.cgi"
