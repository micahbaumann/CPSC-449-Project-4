#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notify', exchange_type='fanout')

mq_msg = {
    "action": "enrolled",
    "uid": 1,
    "class": 1
}
channel.basic_publish(exchange='notify', routing_key='', body=json.dumps(mq_msg), properties=pika.BasicProperties(priority=1))
print(" [x] Sent 'Hello World!'")
connection.close()