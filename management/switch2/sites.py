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
        return "Keine Ger&auml;te gefunden. <a href='/reload'>Reload ausf&uuml;hren.</a>"

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

        rooms = sorted(rooms, key=lambda item: item.get("name"))
        functions = sorted(functions, key=lambda item: item.get("name"))

        return render_template(
                'index.html',
                rooms = rooms,
                functions = functions,
                page_title = app.config['PAGE_TITLE']
                )

@app.route("/obj/<int:object_id>/<path:category>")
@app.route("/obj/<int:object_id>", defaults={"category": "rs"})
def objects_menu(object_id, category):
    get_objects = redis_db0.get('devicelist')
    get_current = redis_db0.get('currentvalues')

    if get_objects == None or get_current == None:
        return "Keine Ger&auml;te gefunden. <a href='/reload'>Reload ausf&uuml;hren.</a>"

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
