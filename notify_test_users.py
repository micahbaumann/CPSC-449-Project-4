import requests
import json
KRAKEND_PORT = 5400

requestBody = {
    "username": "53",
    "password": "12345",
}

req = requests.post(f"http://localhost:{KRAKEND_PORT}/user/login", json=requestBody)
j = req.json()

req = requests.delete(f"http://localhost:{KRAKEND_PORT}/student/unsubscribe/2", headers={
    "Authorization": f"Bearer {j['access_token']}",
    "email_header": "s53@example.com",
    "callback_header": "https://smee.io/I80wU6LZJaxEanl",
    })
j = req.content
print(j)
print()
print()

print("done")