import requests
import json
KRAKEND_PORT = 5400

i = 2
while i < 3:
    requestBody = {
        "username": str(i),
        "password": "12345",
    }

    req = requests.post(f"http://localhost:{KRAKEND_PORT}/user/login", json=requestBody)
    j = req.json()

    req = requests.delete(f"http://localhost:{KRAKEND_PORT}/student/remove/2", headers={"Authorization": f"Bearer {j['access_token']}"})
    j = req.content
    print(j)
    print()
    print()
    i += 1

print("done")