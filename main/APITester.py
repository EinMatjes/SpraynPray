import requests

BASE = "http://192.168.0.16:5000/"

response = requests.put(BASE + "register" ,{"register_ID": 1, "register_Data": 3})

print(response.json())