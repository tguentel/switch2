#!/usr/bin/env python

import sys
import json
import requests
import logging

from time import sleep

sys.path.append("/consumer/bin")
from classes.const import const
import modules.rabbitmqConnect as rabbitmq


queue_name = "switch_command"
delay_name = "control_loop_delay"

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout,
                    format = log_format,
                    level = const.loglevel)
logger = logging.getLogger()


def state_change(ise_id, new_value, retriggered):
    logger.info("ID %s: Changing state to new value %s" % (ise_id, new_value))
    logger.info("ID %s: Retriggered is set to %s" % (ise_id, retriggered))
    url = "%s%s%s/statechange.cgi?ise_id=%s&new_value=%s" % (const.ccu_proto, const.ccu_addr, const.ccu_res, ise_id, new_value)
    r = requests.get(url)

def start_control_loop(ise_id, old_value, new_value):
    logger.info("ID %s: Start control loop" % ise_id)
    rmq_data = {
        "ise_id": ise_id,
        "new_value": new_value,
        "old_value": old_value,
        "retriggered": "false"
        }
    rabbitmq.channel.basic_publish(exchange='', routing_key=delay_name, body=json.dumps(rmq_data))

def consume(ch, method, properties, body):
    msg = json.loads(body)
    state_change(msg['ise_id'], msg['new_value'], msg['retriggered'])
    start_control_loop(msg['ise_id'], msg['old_value'], msg['new_value'])
    ch.basic_ack(delivery_tag = method.delivery_tag)
    sleep(1)

def main():
    logger.info("Starting consumer: execute-change")
    rabbitmq.channel.basic_qos(prefetch_count=1)
    rabbitmq.channel.basic_consume(queue_name, on_message_callback=consume)
    rabbitmq.channel.start_consuming()
    rabbitmq.connection.close()


if __name__ == '__main__':
    main()
