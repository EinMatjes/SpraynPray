from pyModbusTCP.client import ModbusClient
import time
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort


app = Flask(__name__)
api = Api(app)
client = ModbusClient(host="192.168.1.2", port=502, debug=True) #this is the IP of the Easy PLC. !!!Needs to be changed based on Beagle Router Settings / The static ip of the EASY PLC!!!

#adress = 1001 
#number = 1


registers = {}      # Dictionary to store the (Register_ID : Data) Key-Value Pairs

# Adding Arguments for GET Requests 
register_get_args = reqparse.RequestParser()
register_get_args.add_argument("register_ID", type=int, required=True, help="ID of Register is Regquired")  #get requires the register ID to read form the PLC
                                                                                                            #a table with Register ID <-> PLC Function has been Provided with the Project Documentation
# Adding Arguments for PUT Requests 
register_put_args = reqparse.RequestParser()
register_put_args.add_argument("register_ID", type=int, required=True, help="ID of Register is Required")               #PUT requires the register ID and DATA to write to the PLC
register_put_args.add_argument("register_Data", type=int, required=True, help="Write content of Register is Required")  #a table with Register ID <-> PLC Function has been Provided with the Documentation
class holding_register(Resource):
    
    #Defining GET Requests
    def get(self):
        args = register_get_args.parse_args()   #parsing GET Arguments to GET Request
        if not client.open():                   #Checking if the PLC is connected
            abort("Unable to Connect to PLC")
        else:                                   
            registers[args["register_ID"] ] = client.read_holding_registers(args["register_ID"], 1)  #Reading the Marker from the PLC
            print(f"Register Nr: {args['register_ID']} = {registers[args['register_ID']]}")  
      
        return registers[args["register_ID"]]   #return Marker Value
    
    
    def put(self):
        args = register_put_args.parse_args()  #parsing PUT Arguments to PUT Request
        if not client.open(): #Checking if the PLC is connected
            abort("Unable to Connect to PLC")
        else:   

            #Start Cleaning Cycle Function condition check
            if args["register_ID"] == 1003:  #IF the Register ID of the PUT request is 33
                registers[1] = client.read_holding_registers(1001,1) # Reading Marker word 1 (system in Startposition)
                if registers[1][0] != 1: #Checks MarkerWord 1. If MW1 != 1 means System not in Startposition
                    return"Cannot Start Cleaning Cycle: System not in Startposition" #Aborts cause system not in Startposition
                    

            #Nozzle Cleaning Function condition check
            if args["register_ID"] == 1005: # IF the Register ID of the PUT request is 65
                registers[1] = client.read_holding_registers(1001,1) # Reading Marker word 1 (system in Startposition)
                if registers[1][0] != 1: #Checks MarkerWord 1. If MW1 != 1 means System not in Startposition
                    return "Cannot clean nozzle: System not in Startposition" #Aborts cause system not in Startposition

            client.write_single_register(args["register_ID"], args["register_Data"]) # If system in Startposition. Writing the desired Markerword to desiered Data ... (data should normally always be int = 1 )

        return "Succesfully updated"

api.add_resource(holding_register,"/register")
          
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)     
        