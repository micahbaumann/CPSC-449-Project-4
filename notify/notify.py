from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Annotated
import redis
import boto3
import pika
import sys
import json
import smtplib
from email.message import EmailMessage

dynamo_db = boto3.resource('dynamodb', endpoint_url="http://localhost:5500")

classes_table = dynamo_db.Table('Classes')
class Settings(BaseSettings, env_file="users/.env", extra="ignore"):
    logging_config: str

app = FastAPI()

def get_redis():
    yield redis.Redis()

def produce_enrollment_notification(message):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='notis', exchange_type='fanout')

    channel.basic_publish(exchange='notis', routing_key='', body=json.dumps(message))
    print(f" [x] Sent {message} to consumer")
    connection.close()

@app.post("/subscribe/{studentid}/{classid}")
def example(studentid: int, 
            classid: int, 
            email_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            callback_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            r = Depends(get_redis)):

    subscription_key = f"subscription:{studentid}_{classid}"
    
    r.hset(subscription_key,
           mapping={
               "studentid" : studentid,
               "classid" : classid,
               "email_header" : email_header,
               "callback_header" : callback_header
           })
    
    #Left this here just in case you want to see the entry that was just created
    # created_subscription = r.hgetall(subscription_key)
    # return {"created_subscription" : created_subscription}

    return {"message" : "Subscription succesful"}

@app.delete("/unsubscribe/{studentid}/{classid}")
def example(studentid: int, 
            classid: int, 
            email_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            callback_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            r = Depends(get_redis)):

    subscription_key = f"subscription:{studentid}_{classid}"
    
    all_keys = list(r.hgetall(subscription_key).keys())
    r.hdel(subscription_key, *all_keys)

    #Left this here just in case you want to check if key was actually deleted
    # created_subscription = r.hgetall(subscription_key)
    # print(created_subscription)

    return {"message" : "Unsubscription successful"}

@app.get("/subscriptions/{student_id}")
def get_subscriptions(student_id: int, r = Depends(get_redis)):
    pattern = f'subscription:{student_id}_*'
    subscriptions = []
    subscribed_courses=[]
    cursor = '0'
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor, match=pattern)  
        for key in keys:
            subscription_data = r.hgetall(key)
            subscriptions.append(subscription_data.get(b'classid').decode())
        
        if cursor == 0:
            break
        cursor = int(cursor)

        
    for class_id in subscriptions:
        response = classes_table.get_item(
            Key={
                "ClassID": int(class_id)
            }
    )
    
        item = response.get("Item")
        if item:
            class_name = item.get("ClassName")
            if class_name:
                subscribed_courses.append(class_name)



    return {"subscriptions": subscribed_courses}

@app.get("/dummyEnroll")
def enroll_student_in_class(r = Depends(get_redis)):
    studentid = 1
    classid = 1
    subscription_key = f"subscription:{studentid}_{classid}"
    #TO DO
    #Check if subscription key even exists
    subscription_info = r.hgetall(subscription_key)
    stringified_subscription_info = {str(key, 'utf-8'): str(value, 'utf-8') for key, value in subscription_info.items()}
    produce_enrollment_notification(stringified_subscription_info)
    return {}


