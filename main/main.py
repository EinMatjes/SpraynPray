from pyModbusTCP.client import ModbusClient
import time
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort


app = Flask(__name__)
api = Api(app)
client = ModbusClient(host="192.168.0.15", port=502, debug=True)

#adress = 1001 
#number = 1


registers = {}

register_get_args = reqparse.RequestParser()
register_get_args.add_argument("register_ID", type=int, required=True, help="ID of Register is Regquired")

register_put_args = reqparse.RequestParser()
register_put_args.add_argument("register_ID", type=int, required=True, help="ID of Register is Required")
register_put_args.add_argument("register_Data", type=int, required=True, help="Write content of Register is Required")

class holding_register(Resource):
    
    def get(self):
        args = register_get_args.parse_args()
        if not client.open():
            abort("Unable to Connect to PLC")
        else:
            registers[args["register_ID"] ] = client.read_holding_registers(1000 + args["register_ID"], 1)  
            print(f"Register Nr{args['register_ID']} = {registers[args['register_ID']]}")
      
        return registers[args["register_ID"]]
    
    def put(self):
        args = register_put_args.parse_args()  
        if not client.open():
            abort("Unable to Connect to PLC")
        else:
            client.write_single_register(args["register_ID"], args["register_Data"]) 
        return "Succesfully updated"

            



        


   

api.add_resource(holding_register,"/register")
          
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)     
        