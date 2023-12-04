import pika
import smtplib
from email.message import EmailMessage
import json

def send_email(sender, receiver, message):
    msg = EmailMessage()
    msg.set_content(message)

    me = sender
    you = receiver
    msg['Subject'] = 'Enrollment Email Notification'
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP('localhost', 8025)
    s.send_message(msg)
    s.quit()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notis', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='notis', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f"Sending Email with this entry {json.loads(body)}")
    body = json.loads(body)
    message = f"You've just been enrolled to a class, class id : {body['classid']}"
    send_email(sender='school@gmail.com', receiver=body['email_header'], message=message)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()