#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notification', exchange_type='fanout')

mq_msg = {
    "action": "enrolled",
    "uid": 12345,
    "class": 12
}
channel.basic_publish(exchange='notification', routing_key='hello', body=json.dumps(mq_msg))#'Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()