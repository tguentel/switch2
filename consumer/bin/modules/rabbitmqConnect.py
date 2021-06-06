import pika
from time import sleep
from sys import exit

count = 0
status = 1

credentials = pika.PlainCredentials('rabbit', 'RabbitPass21')
parameters = pika.ConnectionParameters(credentials=credentials, host='switch-rabbitmq', virtual_host='/')

while status == 1:
    if count <= 6:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            status = 0
        except:
            count += 1
            sleep(5)
    else:
        print('Error: Cant connect to RabbitMQ. Tried %s times.' % count)
        exit(status)
