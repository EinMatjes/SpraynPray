from pyModbusTCP.client import ModbusClient
import time
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort


app = Flask(__name__)
api = Api(app)
client = ModbusClient(host="192.168.1.4", port=502, debug=True)

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
            registers[args["register_ID"] ] = client.read_holding_registers(args["register_ID"], 1)  
            print(f"Register Nr: {args['register_ID']} = {registers[args['register_ID']]}")
      
        return registers[args["register_ID"]]
    
    def put(self):
        args = register_put_args.parse_args()  #parsing PUT Arguments to PUT Request
        if not client.open(): #Checking if the PLC is connected
            abort("Unable to Connect to PLC")
        else:   
            
            #Start Cleaning Cycle Function condition check
            if args["register_ID"] == 33:  #IF the Register ID of the PUT request is 33
                if client.read_holding_registers(1,1) != 1: #Checks MarkerWord 1. If MW1 != 1 means System not in Startposition.
                    abort("Cannot Start Cleaning Cycle: System not in Startposition") #Aborts with error message

            #Nozzle Cleaning Function condition check
            if args["register_ID"] == 65: # IF the Register ID of the PUT request is 65
                if client.read_holding_registers(1,1) != 1: #Checks MarkerWord 1. If MW1 != 1 means System not in Startposition.
                    abort("Cannot clean nozzle: System not in Startposition") #Aborts with error message


            client.write_single_register(args["register_ID"], args["register_Data"]) # If the System is in adequate Programm State for the Register_ID (corresponding to a Programm function) provided the Data is written to the Register ID specified. This will be 1 for most cases

        return "Succesfully updated"

            



        


   

api.add_resource(holding_register,"/register")
          
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)     
        