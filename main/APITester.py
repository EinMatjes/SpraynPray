import requests

BASE = "http://192.168.0.16:5000/"


response = requests.put(BASE + "register" ,{"register_ID": 1002, "register_Data": 258})

print(response.json())