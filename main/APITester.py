import requests

BASE = "http://192.168.0.16:5000/"

response = requests.put(BASE + "register" ,{"register_ID": 25, "register_Data": 1})

print(response.json())