#! /usr/bin/env python

import pika
import json
import sys

from flask import redirect
from flask import url_for
from flask import request
from switch2 import app
from switch2 import redis_db0


def rabbitmq_produce(msg, queue):
    credentials = pika.PlainCredentials('rabbit', 'RabbitPass21')
    parameters = pika.ConnectionParameters(credentials=credentials, host='switch2-rabbitmq', virtual_host='/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=queue, body=msg)
    connection.close()


@app.route('/produce', methods=['POST'])
def produce():
    control = request.form.getlist('control')
    device = request.form.getlist('device')
    new_value = request.form.getlist('new_value')

    for i in range(len(control)):
        rmq_data = {
                "ise_id": control[i],
                "new_value": new_value[i],
                }
        rabbitmq_produce(json.dumps(rmq_data), "switch_command")

        get_current = redis_db0.get('currentvalues')
        if get_current == None:
            return render_template(
                'reload.html'
                )
        jc = json.loads(get_current)
        jc['values'].update({device[i]: new_value[i]})
        redis_db0.set('currentvalues', json.dumps(jc))

    return redirect("/")
