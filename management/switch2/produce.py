#! /usr/bin/env python

import pika
import json
import sys

from flask import redirect
from flask import url_for
from flask import request
from switch2 import app


def rabbitmq_produce(msg, queue):
    credentials = pika.PlainCredentials('rabbit', 'RabbitPass21')
    parameters = pika.ConnectionParameters(credentials=credentials, host='switch2-rabbitmq', virtual_host='/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=queue, body=msg)
    connection.close()


@app.route('/produce', methods=['POST'])
def produce():
    ise_id = request.form.getlist('ise_id')
    room_id = request.form.getlist('room_id')
    new_value = request.form.getlist('new_value')

    for i in range(len(ise_id)):
        rmq_data = {
                "ise_id": ise_id[i],
                "new_value": new_value[i],
                }
        redirect_target = "/obj/" + room_id[i]
        rabbitmq_produce(json.dumps(rmq_data), "switch_command")

    return redirect(redirect_target)
