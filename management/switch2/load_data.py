#! /usr/bin/env python

import json
import requests
import xml.etree.ElementTree as ET

from flask import render_template

from switch2 import app
from switch2 import redis_db0

@app.route("/reload")
def load_data():
    room_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_ROOMLIST']
    state_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_STATELIST']
    function_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_FUNCTIONLIST']

    r = requests.get(room_url)
    r_root = ET.fromstring(r.text)

    s = requests.get(state_url)
    s_root = ET.fromstring(s.text)

    f = requests.get(function_url)
    f_root = ET.fromstring(f.text)

    roomlist = {'rooms': {}}
    for r in r_root:
        jr = json.loads(str(r.attrib).replace("'",'"'))
        room = jr['ise_id']
        name = jr['name']
        roomlist['rooms'].update({room: {'name': name, 'channels': []}})
        for c in r:
            jc = json.loads(str(c.attrib).replace("'",'"'))
            roomlist['rooms'][room]['channels'].append(jc['ise_id'])

    functionlist = {'functions': {}}
    for f in f_root:
        jf = json.loads(str(f.attrib).replace("'",'"'))
        function = jf['ise_id']
        name = jf['name']
        functionlist['functions'].update({function: {'name': name, 'channels': []}})
        for c in f:
            jc = json.loads(str(c.attrib).replace("'",'"'))
            functionlist['functions'][function]['channels'].append(jc['ise_id'])

    devicelist = {'devices': {}}
    for s in s_root:
        jde = json.loads(str(s.attrib).replace("'",'"'))
        device = jde['ise_id']
        name = jde['name']
        devicelist['devices'].update({device: {'name': name, 'index': {}, 'room': {}, 'function': []}})
        for c in s:
            jdc = json.loads(str(c.attrib).replace("'",'"'))
            index = jdc['index']
            channel = jdc['ise_id']
            model = jdc['name'].split(' ')[0]
            if model.lower() in app.config['HMIP_API_DEVICES']:
                devicelist['devices'][device].update({'model': model.lower()})
                for d in c:
                    jda = json.loads(str(d.attrib).replace("'",'"'))
                    datapoint = jda['ise_id']
                    if jda['type'] in app.config['HMIP_API_TYPES']:
                        devicelist['devices'][device]['index'].update({index: {}})
                        devicelist['devices'][device]['index'][index].update({'channel': channel})
                        devicelist['devices'][device]['index'][index].update({'datapoint': datapoint})
                        for room in roomlist['rooms']:
                            if channel in roomlist['rooms'][room]['channels']:
                                devicelist['devices'][device]['room'].update({
                                    'id': room,
                                    'name': roomlist['rooms'][room]['name']
                                    })
                        for function in functionlist['functions']:
                            if channel in functionlist['functions'][function]['channels']:
                                devicelist['devices'][device]['function'].append({
                                    'id': function,
                                    'name': functionlist['functions'][function]['name']
                                    })

    redis_db0.set("devicelist", json.dumps(devicelist))

    return "Daten neu geladen\n"


def gather_current_values(url):
    s = requests.get(url)
    s_root = ET.fromstring(s.text)

    for s in s_root:
        jda = json.loads(str(s.attrib).replace("'",'"'))
        value = jda['value']

    try:
        float(value)
    except:
        return str(value)
    else:
        return str(round(float(value), 2))

@app.route("/update")
def update_states():
    state_url = app.config['HMIP_API_BASE_URL'] + app.config['HMIP_API_STATE'] + "?datapoint_id=%s"
    devices = redis_db0.get('devicelist')
    currentvalues = {'values': {}}

    if devices == None:
        return "Keine Ger&auml;te gefunden. <a href='/reload'>Reload ausf&uuml;hren.</a>"

    else:
        jde = json.loads(devices)
        for d in jde['devices']:
            try:
                jde['devices'][d]['model']
            except:
                pass
            else:
                if jde['devices'][d]['model'] == "hmip-broll":
                    index = "3"
                elif jde['devices'][d]['model'] == "hmip-bwth" or jde['devices'][d]['model'] == "hmip-wth-2":
                    index = "1"
                elif jde['devices'][d]['model'] == "hmip-psm" or jde['devices'][d]['model'] == "hmip-fsm":
                    index = "2"
                datapoint = jde['devices'][d]['index'][index]['datapoint']
                value = gather_current_values(state_url % datapoint)
                currentvalues['values'].update({d: value })

    redis_db0.set("currentvalues", json.dumps(currentvalues))

    return "Update ausgeführt\n"

