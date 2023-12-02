from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Annotated
import redis

class Settings(BaseSettings, env_file="users/.env", extra="ignore"):
    logging_config: str

app = FastAPI()

def get_redis():
    yield redis.Redis()

# Example Endpoint
@app.get("/example/{ex}")
def example(ex: str):
    return []

@app.get("/subscribe/{studentid}/{classid}")
def example(studentid: int, 
            classid: int, 
            email_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            callback_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            r = Depends(get_redis)):

    subscription_key = f"subscription:{studentid}{classid}"
    
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

@app.get("/unsubscribe/{studentid}/{classid}")
def example(studentid: int, 
            classid: int, 
            email_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            callback_header : Annotated[str | None, Header(convert_underscores=False)] = "None",
            r = Depends(get_redis)):

    subscription_key = f"subscription:{studentid}{classid}"
    
    all_keys = list(r.hgetall(subscription_key).keys())
    r.hdel(subscription_key, *all_keys)

    #Left this here just in case you want to check if key was actually deleted
    # created_subscription = r.hgetall(subscription_key)
    # print(created_subscription)

    return {"message" : "Unsubscription successful"}

@app.get("/subscriptions/{student_id}")
def get_subscriptions(student_id: int, r = Depends(get_redis)):
    pattern = f'subscription:{student_id}*'
    subscriptions = []

    cursor = '0'
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor, match=pattern)  
        for key in keys:
            subscription_data = r.hgetall(key)
            subscriptions.append(subscription_data)
        
        if cursor == 0:
            break
        cursor = int(cursor)

    return {"subscriptions": subscriptions}


