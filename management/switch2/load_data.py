#! /usr/bin/env python

import json
import requests
import xml.etree.ElementTree as ET
import sys

from flask import render_template

from switch2 import app
from switch2 import redis_db0



def make_request(url):
    r = requests.get(url)
    return r.json()

@app.route("/reload")
def load_data():
    room_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_ROOMLIST']
    state_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_STATELIST']
    function_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_FUNCTIONLIST']

    devicelist = {}

    url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_DEVICE_URL']
    devices = make_request(url)
    for device in devices['~links']:
        devicedata = make_request("%s/%s" % (url, device['href']))
        try:
            devicedata['type']
        except:
            pass
        else:
            if devicedata['type'].lower() in app.config['HMIP_API_ALLOWED_DEVICES']:
                d_address = devicedata['address']
                d_type = devicedata['type'].lower()
                d_title = devicedata['title']
                devicelist.update({d_address: {'title': d_title, 'type': d_type, 'room': {}, 'function': {}, 'channel': {}}})
                for d_channel in devicedata['~links']:
                    if d_channel['rel'] == "channel" and d_channel['href'] != "$MASTER":
                        #sys.stdout.write(str(channel['href']))
                        channeldata = make_request("%s/%s/%s" % (url, d_address, d_channel['href']))
                        for c_links in channeldata['~links']:
                            if c_links[]
                            if c_links['rel'] == "room":
                                devicelist[d_address]['room'].update({c_links['href'].replace('/room/',''): c_links['title']})
                            elif c_links['rel'] == "function":
                                devicelist[d_address]['function'].update({c_links['href'].replace('/function/',''): c_links['title']})
                            elif c_links['rel'] == "parameter" and c_links['href'] in app.config['HMIP_API_ALLOWED_TYPES']:
                                parameter = make_request("%s/%s/%s/%s/~pv" % (url, d_address, d_channel['href'], c_links['href'].upper()))
                                devicelist[d_address]['channel'].update
        sys.stdout.write(str(devicelist))

        #for d in devicedata:
            #if devicedata[d]['type'].lower() in app.config['HMIP_API_ALLOWED_DEVICES']:
                #sys.stdout.write(str(devicedata[d]['title']) + "\n")

    #redis_db0.set("devicelist", json.dumps(devicelist))

    return "Daten neu geladen\n"

