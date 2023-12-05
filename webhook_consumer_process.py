#!/usr/bin/env python
import pika
import httpx
import sys
import os
import redis

def main():
    r = redis.Redis()
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='notify', exchange_type='fanout')
    
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    channel.queue_bind(exchange='notify', queue=queue_name)
    
    print(' [*] Waiting for logs. To exit press CTRL+C')
    
    def callback(ch, method, properties, body):
        enrollmentInfo = json.loads(body)
        studentid = enrollmentInfo["uid"]
        classid = enrollmentInfo["class"]
        
        notifyInfo = r.hgetall(f"subscription:{studentid}_{classid}")
        stringified_subscription_info = {str(key, 'utf-8'): str(value, 'utf-8') for key, value in notifyInfo.items()}
        if notifyInfo and stringified_subscription_info["callback_header"]:
            try:
                with httpx.Client() as client:
                    response = client.post(stringified_subscription_info["callback_header"], data=body.decode('utf-8'))
                    if response.is_success:
                        print(f"Webhook notification sent successfully: {body}")
                    else:
                        print(f"Failed to send Webhook notification. Status code: {response.status_code}")
            except Exception as e:
                print(f"Failed to send Webhook notification. Error: {str(e)}")
    
    
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\Webhook consumer process exited')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
