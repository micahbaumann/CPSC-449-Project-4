#!/usr/bin/env python
import pika
import httpx
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notis', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='notis', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body, webhook_url):
    try:
        with httpx.Client() as client:
            response = client.post(webhook_url, data=body.decode('utf-8'))
            if response.is_success:
                print(f"Webhook notification sent successfully: {body}")
            else:
                print(f"Failed to send Webhook notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send Webhook notification. Error: {str(e)}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()