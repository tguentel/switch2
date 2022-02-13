#!/usr/bin/env python

import pika
import json
import requests
import sys

from time import sleep

sys.path.append("/consumer/bin")
from classes.const import const
import modules.rabbitmqConnect as rabbitmq


queue_name = "control_loop"
delay_name = "control_loop_delay"

def declarations():
    rabbitmq.channel.queue_declare(queue=queue_name, durable=False)
    rabbitmq.channel.queue_bind(exchange='amq.direct', queue=queue_name)
    rabbitmq.channel.queue_declare(queue=delay_name, durable=False, arguments={
        'x-message-ttl': 5000,
        'x-dead-letter-exchange': 'amq.direct',
        'x-dead-letter-routing-key': queue_name
    })

def consume(ch, method, properties, body):
    msg = json.loads(body)
    sys.write.stdout("consumed")
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    declarations()
    rabbitmq.channel.basic_qos(prefetch_count=1)
    rabbitmq.channel.basic_consume(queue_name, on_message_callback=consume)
    rabbitmq.channel.start_consuming()
    rabbitmq.connection.close()


if __name__ == '__main__':
    main()
