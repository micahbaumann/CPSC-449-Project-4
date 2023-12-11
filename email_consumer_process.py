#!/usr/bin/env python
import pika
import json
import smtplib
from email.message import EmailMessage
import redis
import sys
import os

def main():
    r = redis.Redis()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='notify', exchange_type='fanout')
    
    result = channel.queue_declare(queue='email')
    queue_name = result.method.queue

    channel.queue_bind(exchange='notify', queue=queue_name)

    print(' [*] Waiting for notify. To exit press CTRL+C')

    def send_email(ch, method, properties, body):
        print(f" [x] New Enrollment: {body}")
        enrollmentInfo = json.loads(body)
        studentid = enrollmentInfo["uid"]
        classid = enrollmentInfo["class"]

        notifyInfo = r.hgetall(f"subscription:{studentid}_{classid}")
        stringified_subscription_info = {str(key, 'utf-8'): str(value, 'utf-8') for key, value in notifyInfo.items()}
        if notifyInfo and stringified_subscription_info["email_header"]:
            msg = EmailMessage()
            msg.set_content(f"Hello student {studentid},\n\nYou have been enrolled in class {classid}.")
            msg["Subject"] = "New Enrollment"
            msg["To"] = stringified_subscription_info["email_header"]
            msg["from"] = "notifications@fullerton.edu"

            try:
                s = smtplib.SMTP('localhost', 8025)
                s.send_message(msg)
                s.quit()
                print(f" [x] Email sent.")
            except:
                print(f" [x] Could not connect to mail server. Email not sent.")
        else:
            print(f" [x] Student or class or email not found. Email not sent.")
        print()

    channel.basic_consume(
        queue=queue_name, on_message_callback=send_email, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nEmail consumer process exited')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)