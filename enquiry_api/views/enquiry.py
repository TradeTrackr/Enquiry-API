from flask import request, Blueprint, jsonify
import boto3
from enquiry_api import config
from enquiry_api.sql import Sql
from datetime import datetime
from botocore.client import Config
from enquiry_api.dependencies.account_api import AccountApi

s3_client = boto3.client('s3',
    aws_access_key_id= config.aws_access_key_id,
    aws_secret_access_key= config.aws_secret_access_key,
    config=Config(signature_version='s3v4'),
    region_name='eu-west-2')


enquiry = Blueprint('enquiry', __name__)

#TODO this should have some kind of authentication
@enquiry.route("/get_enquirys/<company_id>", methods=['GET'])
def get_enquirys(company_id):
    results = Sql.get_enquirys({"company_id": company_id})

    return build_output(results)

@enquiry.route("/get_enquiry/<id>/<company_id>", methods=['GET'])
def get_enquiry(id, company_id):
    results = Sql.get_enquirys({"id": int(id), "company_id": company_id})
    result_dict = []
    for key in results:
        output = key.to_dict()
        if output.get('photos',{}) is not {}:
            photos_url={}
            for key in output['photos']:
                key_val ='{}/homefrontmaintenance/{}/{}/{}'.format(config.BUCKET_NAME,
                                                                output.get('full_name').replace(' ','').lower(),
                                                                id,
                                                                key
                                                                )

                url = s3_client.generate_presigned_url('get_object',
                                                        Params = {
                                                                    'Bucket': config.BUCKET_ID,
                                                                    'Key':key_val
                                                                }, ExpiresIn = 3600)
                photos_url.update({key: url})
            output['photos'] = photos_url

        result_dict.append(output)
    
    return jsonify(result_dict)


@enquiry.route("/new_enquiry", methods=['POST'])
def new_enquiry():
    json_data = request.json
    #replace this..
    # do a check that company id is in account_api
    # check_company_bool = AccountApi().get_company(json_data.get('company_id'))
    # if check_company_bool == True:

    if json_data.get('company_id') == '0f40cbf6-3502-4836-b548-37e864eec836':

        results = Sql.new_enquiry(json_data)
        return build_output(results)

    else:
        #TODO error is returned with a 200 status code
        return jsonify({'error': '403', 'error_message': 'company_id is not valid'})

@enquiry.route('/generate_presigned_url', methods=['POST'])
def generate_presigned_url():
    json_data = request.json
    #replace this..
    # do a check that company id is in account_api
    if json_data.get('company_id') == '0f40cbf6-3502-4836-b548-37e864eec836':
    
        # replace with company name based on company id..
        bucket_name = config.BUCKET_ID
        files_info = request.json.get("file_names")

        # Define the presigned URL expiration time
        expiration = 6000  # seconds

        presigned_urls = []

        for file_info in files_info:
            key_val ='{}/homefrontmaintenance/{}/{}/{}'.format(config.BUCKET_NAME,
                                                            json_data.get('fullname').replace(' ','').lower(),
                                                            json_data.get('enquiry_id'),
                                                            file_info
                                                            )
            # Generate a presigned URL for each file
            presigned_url = s3_client.generate_presigned_url('put_object',
                                                            Params={'Bucket': bucket_name,
                                                                    'Key': key_val},
                                                            ExpiresIn=expiration)
            presigned_urls.append({'file_name': file_info, 'presigned_url': presigned_url})

        return jsonify({'presigned_urls': presigned_urls})

    else:
        #TODO error is returned with a 200 status code
        return jsonify({'error': '403', 'error_message': 'company_id is not valid'})


def build_output(results):
    result_dict = []
    for key in results:
        output = key.to_dict()
        result_dict.append(output)
    return jsonify(result_dict)
