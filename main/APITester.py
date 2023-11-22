import requests

BASE = "http://192.168.1.3:5000/"


response = requests.put(BASE + "register" ,{"register_ID": 1002, "register_Data": 258})

print(response.json())