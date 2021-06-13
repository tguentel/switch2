#! /usr/bin/env python

import json

from flask import render_template

from switch2 import app
from switch2 import redis_db0


@app.route("/")
def main_menu():
    rooms = []
    get_rooms = redis_db0.get('rooms')
    if get_rooms == None:
        return render_template(
                'reload.html'
                )
    else:
        for r in json.loads(get_rooms)['rooms']:
            if 'devices' in r:
                rooms.append([ r['room_id'], r['desc'] ])
        return render_template(
                'index.html',
                rooms = rooms
                )

@app.route("/rooms/<int:room_id>")
def rooms_menu(room_id):
    get_rooms = redis_db0.get('rooms')
    for r in json.loads(get_rooms)['rooms']:
        if r['room_id'] == room_id:
            room_data = [ r['room_id'], r['desc'], r['devices'] ]
            return render_template(
                'rooms.html',
                room_data = room_data
                )
