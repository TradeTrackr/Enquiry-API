from flask import request, Blueprint, jsonify
from enquiry_api.sql import Sql
from datetime import datetime


enquiry = Blueprint('enquiry', __name__)


@enquiry.route("/get_enquirys/<id>", methods=['GET'])
def get_enquirys(id):

    results = Sql.get_all_enquirys({"company_id": id})

    return build_output(results)


@enquiry.route("/new_enquiry", methods=['POST'])
def new_enquiry():
    json_data = request.json

    timestamp = datetime.now()
    json_data2 = {'enquiry_timestamp' : timestamp}
    json_data.update(json_data2)

    results = Sql.new_enquiry(json_data)
    return build_output(results)


def build_output(results):
    result_dict = []
    for key in results:
        output = key.to_dict()
        result_dict.append(output)
    return jsonify(result_dict)
