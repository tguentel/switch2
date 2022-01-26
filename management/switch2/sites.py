#! /usr/bin/env python

import json
import sys

from flask import render_template

from switch2 import app
from switch2 import redis_db0


def get_navstart(room_id):
    if room_id in app.config['NAVSTART_EXCEPTION']:
        navstart = app.config['NAVSTART_EXCEPTION'][room_id]
    else:
        navstart = "rs"
    return navstart

@app.route("/")
def main_menu():
    devices = redis_db0.get('devicelist')
    if devices == None:
        return "Keine Ger&auml;te gefunden. <a href='/reload'>Reload ausf&uuml;hren.</a>"

    else:
        jd = json.loads(devices)
        rooms = []
        r_seen = []
        navstart = None
        for r in jd['devices']:
            room_info = jd['devices'][r]['room']
            if room_info != {}:
                room_id = room_info['id']
                if room_id not in r_seen:
                    r_seen.append(room_id)
                    model = jd['devices'][r]['model']
                    navstart = get_navstart(room_id)
                    room_info.update({'navstart': navstart})
                    rooms.append(room_info)

        f_seen = []
        functions = []
        navstart = None
        for d in jd['devices']:
            function_all = jd['devices'][d]['function']
            if function_all != []:
                for f in function_all:
                    function_id = f['id']
                    if str(function_id) not in f_seen:
                        f_seen.append(function_id)
                        model = jd['devices'][d]['model']
                        navstart = get_navstart(room_id)
                        f.update({'navstart': navstart})
                        functions.append(f)

        rooms = sorted(rooms, key=lambda item: item.get("name"))
        functions = sorted(functions, key=lambda item: item.get("name"))

        return render_template(
                'index.html',
                rooms = rooms,
                functions = functions,
                page_title = app.config['PAGE_TITLE']
                )

@app.route("/obj/<int:object_id>/<string:category>/")
def objects_menu(object_id, category):
    get_objects = redis_db0.get('devicelist')
    get_current = redis_db0.get('currentvalues')

    if get_objects == None:
        return "Keine Ger&auml;te gefunden. <a href='/reload'>Reload ausf&uuml;hren.</a>"
    elif get_current == None:
        return "Keine Ger&auml;tedaten gefunden. <a href='/update'>Update ausf&uuml;hren.</a>"

    jo = json.loads(get_objects)
    jc = json.loads(get_current)

    object_data = []
    for o in jo['devices']:
        try:
            jo['devices'][o]['room']['id']
        except:
            pass
        else:
            if int(jo['devices'][o]['room']['id']) == object_id:
                try:
                    jc['values'][o]
                except:
                    pass
                else:
                    current = jc['values'][o]
                    jo['devices'][o].update({'current': current })
                    jo['devices'][o].update({'device': o })
                    object_data.append(jo['devices'][o])
            for of in jo['devices'][o]['function']:
                if int(of['id']) == object_id:
                    try:
                        jc['values'][o]
                    except:
                        pass
                    else:
                        current = jc['values'][o]
                        jo['devices'][o].update({'current': current })
                        jo['devices'][o].update({'device': o })
                        object_data.append(jo['devices'][o])

    return render_template(
        'object.html',
        object_data = object_data,
        object_id = object_id,
        category = category,
        page_title = app.config['PAGE_TITLE']
        )
