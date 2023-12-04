import smtplib
from email.message import EmailMessage

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

send_email('jorge@gmail.com', 'smorge@gmail.com', "You've been enrolled!")
