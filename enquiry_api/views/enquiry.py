from flask import request, Blueprint, jsonify
import boto3

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
    #replace this..
    # do a check that company id is in account_api

    if json_data.get('company_id') == '0f40cbf6-3502-4836-b548-37e864eec836':

        timestamp = datetime.now()
        json_data2 = {'enquiry_timestamp' : timestamp}
        json_data.update(json_data2)

        results = Sql.new_enquiry(json_data)
        return build_output(results)

    else:
        return jsonify({'error': '403', 'error_message': 'company_id is not valid'})


s3_client = boto3.client('s3')

@enquiry.route('/generate_presigned_url', methods=['POST'])
def generate_presigned_url():
    json_data = request.json
    #replace this..
    # do a check that company id is in account_api
    
    if json_data.get('company_id') == '0f40cbf6-3502-4836-b548-37e864eec836':
    
        # replace with company name based on company id..
        bucket_name = 'homefrontmaintenance'
        files_info = request.json.get('upload_imgs[]')

        # Define the presigned URL expiration time
        expiration = 600  # seconds

        presigned_urls = []

        for file_info in files_info:

            # Generate a presigned URL for each file
            presigned_url = s3_client.generate_presigned_url('put_object',
                                                            Params={'Bucket': bucket_name,
                                                                    'Key': file_info},
                                                            ExpiresIn=expiration)
            presigned_urls.append({'file_name': file_info, 'presigned_url': presigned_url})

        return jsonify({'presigned_urls': presigned_urls})

    else:
        return jsonify({'error': '403', 'error_message': 'company_id is not valid'})


def build_output(results):
    result_dict = []
    for key in results:
        output = key.to_dict()
        result_dict.append(output)
    return jsonify(result_dict)
