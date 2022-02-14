#!/usr/bin/env python

import sys
import pika
import logging

sys.path.append("/consumer/bin")
from classes.const import const
import modules.rabbitmqConnect as rabbitmq

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout,
                    format = log_format,
                    level = logging.INFO)
logger = logging.getLogger()

def declare_control_loop(queue_name, durable, ttl, exchange):
    logger.info("Declare everything for %s" % queue_name)
    rabbitmq.channel.queue_declare(queue=queue_name, durable=durable)
    rabbitmq.channel.queue_bind(exchange=exchange, queue=queue_name)
    rabbitmq.channel.queue_declare(queue=queue_name + "_delay", durable=durable, arguments={
        'x-message-ttl': ttl,
        'x-dead-letter-exchange': exchange,
        'x-dead-letter-routing-key': queue_name
    })

def declare_switch_command(queue_name, durable):
    logger.info("Declare everything for %s" % queue_name)
    rabbitmq.channel.queue_declare(queue=queue_name, durable=durable)

def main():
    logger.info("Setting up RabbitMQ")
    declare_switch_command("switch_command", False)
    declare_control_loop("control_loop", False, 30000, "amq.direct")
    exit(0)

if __name__ == "__main__":
    main()
