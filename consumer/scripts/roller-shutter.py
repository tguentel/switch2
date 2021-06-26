#!/usr/bin/env python

import pika
import json
import requests
import sys

sys.path.append("/consumer/bin")
from classes.const import const
import modules.rabbitmqConnect as rabbitmq


queue_name = "switch_command"

def declarations():
    rabbitmq.channel.queue_declare(queue=queue_name, durable=False)

def statechange(id, ise_id, new_value):
    url = "%s%s%s/statechange.cgi?ise_id=%s&new_value=%s" % (const.ccu_proto, const.ccu_addr, const.ccu_res, ise_id, new_value)
    r = requests.get(url)

def consume(ch, method, properties, body):
    msg = json.loads(body)
    statechange(msg['ise_id'], msg['new_value'])
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    declarations()
    rabbitmq.channel.basic_consume(queue_name, on_message_callback=consume)
    rabbitmq.channel.start_consuming()
    rabbitmq.connection.close()


if __name__ == '__main__':
    main()
