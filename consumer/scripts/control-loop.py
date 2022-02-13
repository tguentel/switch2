#!/usr/bin/env python

import pika
import json
import requests
import logging
import xml.etree.ElementTree as ET
import sys

from time import sleep

sys.path.append("/consumer/bin")
from classes.const import const
import modules.rabbitmqConnect as rabbitmq


queue_name = "control_loop"
delay_name = "control_loop_delay"
publish_name = "switch_command"

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout,
                    format = log_format,
                    level = logging.INFO)
logger = logging.getLogger()

def declarations():
    rabbitmq.channel.queue_declare(queue=queue_name, durable=False)
    rabbitmq.channel.queue_bind(exchange='amq.direct', queue=queue_name)
    rabbitmq.channel.queue_declare(queue=delay_name, durable=False, arguments={
        'x-message-ttl': 30000,
        'x-dead-letter-exchange': 'amq.direct',
        'x-dead-letter-routing-key': queue_name
    })

def get_actual_state(ise_id):
    url = "%s%s%s/state.cgi?datapoint_id=%s" % (const.ccu_proto, const.ccu_addr, const.ccu_res, ise_id)
    s = requests.get(url)
    s_root = ET.fromstring(s.text)
    for s in s_root:
        jda = json.loads(str(s.attrib).replace("'",'"'))
        value = jda['value']
    try:
        float(value)
    except:
        return str(value)
    else:
        return str(round(float(value), 2))

def check_value_changes(old_value, new_value, actual_value):
    retrigger = "false"
    if actual_value == old_value:
        logger.error("Value of %s has not changed" % old_value)
        retrigger = "true"
    elif actual_value == new_value:
        logger.info("New value of %s is in place" % new_value)
    elif actual_value != old_value and actual_value != new_value:
        logger.info("Old value of %s has changed to %s but new value of %s is not yet in place" %(old_value, actual_value, new_value))
    else:
        logger.error("Value check was not successful")
    return retrigger

def retrigger_publish_message(ise_id, old_value, new_value):
    logger.info("Republish message to reach the disired state")
    rmq_data = {
        "ise_id": ise_id,
        "new_value": new_value,
        "old_value": old_value,
        "retriggered": "true"
        }
    rabbitmq.channel.basic_publish(exchange='', routing_key=publish_name, body=json.dumps(rmq_data))
    rabbitmq.channel.basic_publish(exchange='', routing_key=delay_name, body=json.dumps(rmq_data))

def consume(ch, method, properties, body):
    msg = json.loads(body)
    actual_value = get_actual_state(msg['ise_id'])
    retrigger = check_value_changes(msg['old_value'], msg['new_value'], actual_value)
    logger.info("Retrigger: %s" % retrigger)
    if retrigger == "true":
        retrigger_publish_message(msg['ise_id'], msg['old_value'], msg['new_value'])
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    logger.info("Starting consumer: control-loop")
    declarations()
    rabbitmq.channel.basic_qos(prefetch_count=1)
    rabbitmq.channel.basic_consume(queue_name, on_message_callback=consume)
    rabbitmq.channel.start_consuming()
    rabbitmq.connection.close()


if __name__ == '__main__':
    main()
