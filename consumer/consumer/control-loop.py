#!/usr/bin/env python

import sys
import json
import requests
import logging
import xml.etree.ElementTree as ET

from time import sleep

sys.path.append("/consumer/bin")
from classes.const import const
import modules.rabbitmqConnect as rabbitmq

from modules.redisConnect import read as redisread


queue_name = "control_loop"
delay_name = "control_loop_delay"
publish_name = "switch_command"

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout,
                    format = log_format,
                    level = const.loglevel)
logger = logging.getLogger()


def get_actual_state(ise_id):
    url = "%s%s%s/state.cgi?datapoint_id=%s" % (const.ccu_proto, const.ccu_addr, const.ccu_res, ise_id)
    s = requests.get(url)
    s_root = ET.fromstring(s.text)
    for s in s_root:
        jda = json.loads(str(s.attrib).replace("'",'"'))
        value = jda['value']
        if value == "true":
            nobool = 1.0
        elif value == "false":
            nobool = 0.0
        else:
            nobool = value
    try:
        float(nobool)
    except:
        return str(nobool)
    else:
        return str(round(float(nobool), 2))

def check_value_changes(ise_id, old_value, new_value, actual_value):
    retrigger = "false"
    if actual_value == old_value:
        logger.error("ID %s: Value of %s has not changed" % (ise_id, old_value))
        retrigger = "true"
    elif actual_value == new_value:
        logger.info("ID %s: New value of %s is in place" % (ise_id, new_value))
    elif actual_value != old_value and actual_value != new_value:
        logger.info("ID %s: Old value of %s has changed to %s but new value of %s is not yet in place" % (ise_id, old_value, actual_value, new_value))
    else:
        logger.error("ID %s: Value check was not successful" % ise_id)
    return retrigger

def retrigger_publish_message(ise_id, old_value, new_value, control_loop_value):
    logger.info("ID: %s: Republish message to reach the disired state" % ise_id)
    rmq_data = {
        "ise_id": ise_id,
        "new_value": new_value,
        "old_value": old_value,
        "retriggered": "true",
        "control_loop_value": control_loop_value
        }
    rabbitmq.channel.basic_publish(exchange='', routing_key=publish_name, body=json.dumps(rmq_data))
    rabbitmq.channel.basic_publish(exchange='', routing_key=delay_name, body=json.dumps(rmq_data))

def check_latest_loop(ise_id, control_loop_value):
    control_loop_value_expected = redisread(ise_id, const.redishost, const.redisport, const.redisdb).decode('utf-8')
    try:
        control_loop_value_expected
        logger.info("ID %s: Found control loop value %s in database" % (ise_id, control_loop_value_expected))
    except:
        logger.error("ID %s: No control loop value found in database" % ise_id)
        return "value_not_found"

    if control_loop_value == control_loop_value_expected:
        logger.info("ID %s: Executing control loop with latest value %s" % (ise_id, control_loop_value))
        return "value_match"
    else:
        logger.error("ID %s: Aborting control loop with value %s due to unexpected value %s" % (ise_id, control_loop_value_expected, control_loop_value))
        return "value_missmatch"

def consume(ch, method, properties, body):
    msg = json.loads(body)
    is_latest = check_latest_loop(msg['ise_id'], msg['control_loop_value'])
    if is_latest == "value_match":
        actual_value = get_actual_state(msg['ise_id'])
        retrigger = check_value_changes(msg['ise_id'], msg['old_value'], msg['new_value'], actual_value)
        logger.info("ID %s: Retrigger set to %s" % (msg['ise_id'], retrigger))
        if retrigger == "true":
            if msg['retriggered'] == "true":
                logger.error("ID %s: Message was retriggered before - giving up" % msg['ise_id'])
            else:
                retrigger_publish_message(msg['ise_id'], msg['old_value'], msg['new_value'], msg['control_loop_value'])
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    logger.info("Starting consumer: control-loop")
    rabbitmq.channel.basic_qos(prefetch_count=1)
    rabbitmq.channel.basic_consume(queue_name, on_message_callback=consume)
    rabbitmq.channel.start_consuming()
    rabbitmq.connection.close()


if __name__ == '__main__':
    main()
