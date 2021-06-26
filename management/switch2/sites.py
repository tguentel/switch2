#! /usr/bin/env python

import json
import sys

from flask import render_template

from switch2 import app
from switch2 import redis_db0


@app.route("/")
def main_menu():
    get_rooms = redis_db0.get('devicelist')
    if get_rooms == None:
        return render_template(
                'reload.html'
                )
    else:
        jr = json.loads(get_rooms)
        rooms = []
        for r in jr['devices']:
            try:
                jr['devices'][r]['room']
            except:
                pass
            else:
                if jr['devices'][r]['room'] not in rooms:
                    rooms.append(jr['devices'][r]['room'])
        rooms = sorted(rooms, key=lambda item: item.get("name"))
        return render_template(
                'index.html',
                rooms = rooms,
                page_title = app.config['PAGE_TITLE']
                )

@app.route("/room/<int:room_id>")
def rooms_menu(room_id):
    get_rooms = redis_db0.get('devicelist')
    get_current = redis_db0.get('currentvalues')

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
                    room_data.append(jr['devices'][r])

    return render_template(
        'rooms.html',
        room_data = room_data,
        page_title = app.config['PAGE_TITLE'],
        rs_initial_value = app.config['RS_INITIAL_VALUE'],
        th_initial_value = app.config['TH_INITIAL_VALUE']
        )
