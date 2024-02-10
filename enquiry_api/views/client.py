import json
from flask import request, Blueprint
from enquiry_api.sql import Sql

client = Blueprint('client', __name__)

@client.route("/client/get_enquirys", methods=['GET'])
def client_get_enquirys():

    json_data = request.json

    results = Sql.get_enquirys(json_data)    

    return build_output(results)

def build_output(results):
    result_dict = []
    for key in results:
        output = key.to_dict()
        result_dict.append(output)
    return result_dict
