#! /usr/bin/env python

import json
import sys

from flask import render_template

from switch2 import app
from switch2 import redis_db0


@app.route("/")
def main_menu():
    devices = redis_db0.get('devicelist')
    if devices == None:
        return render_template(
                'reload.html'
                )
    else:
        jd = json.loads(devices)
        rooms = []
        for r in jd['devices']:
           if jd['devices'][r]['room'] != {}:
               if jd['devices'][r]['room'] not in rooms:
                   rooms.append(jd['devices'][r]['room'])

        functions = []
        for f in jd['devices']:
            if jd['devices'][f]['function'] != []:
                for fd in jd['devices'][f]['function']:
                    if fd not in functions:
                        functions.append(fd)

        sys.stdout.write(str(rooms))

        rooms = sorted(rooms, key=lambda item: item.get("name"))
        functions = sorted(functions, key=lambda item: item.get("name"))

        return render_template(
                'index.html',

                rooms = rooms,
                functions = functions,
                page_title = app.config['PAGE_TITLE']
                )

@app.route("/obj/<int:room_id>")
def rooms_menu(room_id):
    get_rooms = redis_db0.get('devicelist')
    get_current = redis_db0.get('currentvalues')

    if get_rooms == None or get_current == None:
        return render_template(
            'reload.html'
            )

    jr = json.loads(get_rooms)
    jc = json.loads(get_current)

    room_data = []
    for r in jr['devices']:
        try:
            jr['devices'][r]['room']['id']
        except:
            pass
        else:
            if int(jr['devices'][r]['room']['id']) == room_id:
                try:
                    jc['values'][r]
                except:
                    pass
                else:
                    current = jc['values'][r]
                    jr['devices'][r].update({'current': current })
                    jr['devices'][r].update({'device': r })
                    room_data.append(jr['devices'][r])

    return render_template(
        'rooms.html',
        room_data = room_data,
        page_title = app.config['PAGE_TITLE']
        )
