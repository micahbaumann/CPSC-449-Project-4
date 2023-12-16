import requests
import json
KRAKEND_PORT = 5400

i = 0
while i < 100:
    requestBody = {
        "username": str(i),
        "password": "12345",
        "roles": ["Student",],
        "name": str(i),
        "email": f"student{str(i)}@example.com"
    }

    req = requests.post(f"http://localhost:{KRAKEND_PORT}/user/register/", json=requestBody)
    j = req.json()
    print(j)
    print()
    print()
    i += 1

print("done")