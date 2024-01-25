import requests

BASE = "http://192.168.1.3:5000/"

response = requests.put(BASE + "register" ,{"register_ID": 1005, "register_Data": 1})
#response = requests.get(BASE + "register" ,{"register_ID": 1001})

print(response.json())