import requests

BASE = "http://192.168.1.3:5000/" # !!! This is the IP of the RasPi. Change the IP as nececarry for the hangar. Port stays the same.

response = requests.put(BASE + "register" ,{"register_ID": 1005, "register_Data": 1}) #Example for put request. Used to send control messages/set control variables
#response = requests.get(BASE + "register" ,{"register_ID": 1001}) #Example get request. Used to read control variables

print(response.json())  #Prints the response of the request.