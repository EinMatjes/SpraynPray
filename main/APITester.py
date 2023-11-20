import requests

BASE = "http://192.168.0.16:5000/"


response = requests.get(BASE + "register" ,{"register_ID": 1 })

print(response.json())