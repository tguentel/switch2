#! /usr/bin/env python

import pika
import json
import sys
import logging

from flask import redirect
from flask import url_for
from flask import request
from switch2 import app
from switch2 import redis_db0

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout,
                    format = log_format,
                    level = app.config['LOGLEVEL'])
logger = logging.getLogger()


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

    for i in range(len(control)):
        get_current = redis_db0.get('currentvalues')
        if get_current == None:
            return "Keine Ger&auml;te gefunden. <a href='/reload'>Reload ausf&uuml;hren.</a>"

        jc = json.loads(get_current)

        ise_id = control[i]
        new_value = str(float(request.form.getlist('new_value_' + device[i])[0]))
        old_value = jc['values'][device[i]]

        if new_value != old_value:
            logger.info("ID %s: New value %s differs from old value %s" % (ise_id, new_value, old_value))
            logger.info("ID %s: Producing message" % ise_id)
            rmq_data = {
                    "ise_id": ise_id,
                    "new_value": new_value,
                    "old_value": old_value,
                    "retriggered": "false"
                    }
            rabbitmq_produce(json.dumps(rmq_data), "switch_command")

            jc['values'].update({device[i]: new_value})
            redis_db0.set('currentvalues', json.dumps(jc))

        else:
            logger.info("ID %s: New value %s is the same as the old value" % (ise_id, new_value))
            logger.info("ID %s: Nothing to do" % ise_id)
    return redirect(request.referrer)
