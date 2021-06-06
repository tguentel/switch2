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
    id = request.form.get("id")
    ise_id = request.form.get("ise_id")
    new_value = request.form.get("new_value")
    room_id = request.form.get("room_id")
    redirect_target = "/rooms/" + room_id
    rmq_data = {
            "id": id,
            "ise_id": ise_id,
            "new_value": new_value,
            }
    rabbitmq_produce(json.dumps(rmq_data), "switch_command")
    return redirect(redirect_target)
