import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "register" ,{"register_ID": 1, "register_Data": 3})

print(response.json())