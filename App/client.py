import requests
BASE = "http://127.0.0.1:5000/"

for _ in range(5):
    msg = input("User: ")
    response = requests.post(BASE+"/reply", json={"data": msg})
    print(response.json())