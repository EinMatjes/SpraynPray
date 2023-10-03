import requests

BASE = "http://192.168.0.14:5000/"

response = requests.put(BASE + "video/1" ,{"likes": 10, "name": "Mama", "views": 33})
input()
response = requests.get(BASE + "video/1")
print(response.json())
