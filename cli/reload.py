#!/usr/bin/env python

import json
import re
import requests
import xml.etree.ElementTree as ET

def main():
    room_url = "http://192.168.54.75/addons/xmlapi/roomlist.cgi"
    state_url = "http://192.168.54.75/addons/xmlapi/statelist.cgi"
    hmip_api_devices = ["HmIP-BROLL", "HmIP-BWTH"]
    hmip_api_types = ['LEVEL', 'SET_POINT_TEMPERATURE']

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

    devicelist = {'device': {}}
    for s in s_root:
        jde = json.loads(str(s.attrib).replace("'",'"'))
        device = jde['ise_id']
        name = jde['name']
        devicelist['device'].update({device: {'name': name, 'index': {}}})
        for c in s:
            jdc = json.loads(str(c.attrib).replace("'",'"'))
            index = jdc['index']
            channel = jdc['ise_id']
            model = jdc['name'].split(' ')[0]
            if model in hmip_api_devices:
                devicelist['device'][device].update({'model': model})
                for d in c:
                    jda = json.loads(str(d.attrib).replace("'",'"'))
                    datapoint = jda['ise_id']
                    if jda['type'] in hmip_api_types:
                        devicelist['device'][device]['index'].update({index: {}})
                        devicelist['device'][device]['index'][index].update({'channel': channel})
                        devicelist['device'][device]['index'][index].update({'datapoint': datapoint})
                        for room in roomlist['rooms']:
                            print()
                            print('')
                            if channel in roomlist['rooms'][room]['channels']:
                                devicelist['device'][device].update({'room': {
                                    'id': room,
                                    'name': roomlist['rooms'][room]['name']
                                    }})

    print(json.dumps(devicelist))


if __name__ == '__main__':
    main()
