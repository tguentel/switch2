#! /usr/bin/env python

import json
import requests
import xml.etree.ElementTree as ET

from flask import redirect

from switch2 import app
from switch2 import redis_db0

@app.route("/reload")
def load_data():
    room_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_ROOMLIST']
    state_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_STATELIST']

    r = requests.get(room_url)
    r_root = ET.fromstring(r.text)

    s = requests.get(state_url)
    s_root = ET.fromstring(s.text)

    roomlist = {'rooms': {}}
    for r in r_root:
        jr = json.loads(str(r.attrib).replace("'",'"'))
        room = jr['ise_id']
        name = jr['name']
        roomlist['rooms'].update({room: {'name': name, 'channels': []}})
        for c in r:
            jc = json.loads(str(c.attrib).replace("'",'"'))
            roomlist['rooms'][room]['channels'].append(jc['ise_id'])

    devicelist = {'devices': {}}
    for s in s_root:
        jde = json.loads(str(s.attrib).replace("'",'"'))
        device = jde['ise_id']
        name = jde['name']
        devicelist['devices'].update({device: {'name': name, 'index': {}}})
        for c in s:
            jdc = json.loads(str(c.attrib).replace("'",'"'))
            index = jdc['index']
            channel = jdc['ise_id']
            model = jdc['name'].split(' ')[0]
            if model in app.config['HMIP_API_DEVICES']:
                devicelist['devices'][device].update({'model': model})
                for d in c:
                    jda = json.loads(str(d.attrib).replace("'",'"'))
                    datapoint = jda['ise_id']
                    if jda['type'] in app.config['HMIP_API_TYPES']:
                        devicelist['devices'][device]['index'].update({index: {}})
                        devicelist['devices'][device]['index'][index].update({'channel': channel})
                        devicelist['devices'][device]['index'][index].update({'datapoint': datapoint})
                        for room in roomlist['rooms']:
                            print()
                            print('')
                            if channel in roomlist['rooms'][room]['channels']:
                                devicelist['devices'][device].update({'room': {
                                    'id': room,
                                    'name': roomlist['rooms'][room]['name']
                                    }})

    redis_db0.set("devicelist", json.dumps(devicelist))

    return redirect("/")
