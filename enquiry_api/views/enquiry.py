import json
from flask import request, Blueprint, jsonify
import boto3
from enquiry_api import config
from enquiry_api.sql import Sql
from datetime import datetime
from botocore.client import Config
from enquiry_api.dependencies.account_api import AccountApi
from enquiry_api.utilities.authentication import token_required
from enquiry_api.dependencies.sqs import EmailSqsSender
from itsdangerous import URLSafeTimedSerializer

s3_client_limted = boto3.client('s3',
    aws_access_key_id= config.aws_access_key_id_LIMITED,
    aws_secret_access_key= config.aws_secret_access_key_LIMITED,
    config=Config(signature_version='s3v4'),
    region_name='eu-west-2')

s3_client = boto3.client('s3',
    aws_access_key_id= config.aws_access_key_id,
    aws_secret_access_key= config.aws_secret_access_key,
    config=Config(signature_version='s3v4'),
    region_name='eu-west-2')

enquiry = Blueprint('enquiry', __name__)


@enquiry.route("/get_enquirys/<company_id>", methods=['GET'])
@token_required
def get_enquirys(company_id):
    results = Sql.get_enquirys({"company_id": company_id})

    return build_output(results)


@enquiry.route("/get_new_enquirys/<company_id>", methods=['GET'])
@token_required
def get_new_enquirys(company_id):
    results = Sql.get_new_enquiries(company_id)
    return build_output(results)


@enquiry.route("/get_enquiry_to_check", methods=['GET'])
@token_required
def get_enquiry_to_check():

    json_data = request.json

    results = Sql.get_enquirys(json_data)

    return build_output(results)


@enquiry.route("/get_enquiry/<id>/<company_id>", methods=['GET'])
@token_required
def get_enquiry(id, company_id):

    results = Sql.get_enquiry_and_activity({"id": int(id), "company_id": str(company_id)})

    enquiries_list = []
    for enquiry, activity in results:
        enquiries_dict = enquiry.to_dict()
        if enquiries_dict.get('photos',{}) is not {}:
            photos_url={}
            for key in enquiries_dict['photos']:
                key_val ='{}/homefrontmaintenance/{}/{}/{}'.format(config.BUCKET_NAME,
                                                                enquiries_dict.get('full_name').replace(' ','').lower(),
                                                                id,
                                                                key
                                                                )

                url = s3_client.generate_presigned_url('get_object',
                                                        Params = {
                                                                    'Bucket': config.BUCKET_ID,
                                                                    'Key':key_val
                                                                }, ExpiresIn = 3600)
                photos_url.update({key: url})
            enquiries_dict['photos'] = photos_url

        enquiries_dict['activities'] = []

        if activity:
            enquiries_dict['activities'].append(activity.to_dict())

        enquiries_list.append(enquiries_dict)

    return jsonify(enquiries_list)


@enquiry.route("/get_user_enquiries/<company_id>", methods=['GET'])
@token_required
def get_user_enquiries(company_id):
    json_data = request.json

    results = Sql.get_enquirys_most_recent_activity({"email": json_data['email'], "company_id": str(company_id)})

    return jsonify(results)

@enquiry.route("/enquiry/<id>", methods=['PUT'])
@token_required
def update_enquiry(id):
    json_data = request.json

    result = Sql.update_enquiry(id, json_data)

    return build_output(result)


@enquiry.route("/new_enquiry_activity", methods=['POST'])
@token_required
def new_enquiry_activity():
    json_data = request.json

    result = Sql.new_enquiry_activity(json_data)

    return build_output(result)


@enquiry.route("/new_enquiry", methods=['POST'])
def new_enquiry():
    json_data = request.json

    #replace this..
    # do a check that company id is in account_api
    get_company_details = AccountApi().get_company(json_data.get('company_id'))
    if get_company_details != False:
        get_company_details = json.loads(get_company_details)
        results = Sql.new_enquiry(json_data)
        output = build_output(results)
        
        enquiry = {
            "enquiry_id": output[0]['id'],
            "status": "Enquiry Created"
        }
        Sql.new_enquiry_activity(enquiry)

        formatted_address =  f"{json_data['address_line1']}, {json_data['address_line2']}, {json_data['postcode']}"
        # serializer = URLSafeTimedSerializer(config.SECRET_KEY)
        # token = serializer.dumps(json_data['email'], salt='email-confirm')

        EmailSqsSender().send_message({
            "type": "New Enquiry",
            "enquiry_id": output[0]['id'],
            "email": json_data['email'],
            "formatted_address": formatted_address,
            "from_email": get_company_details['company_response_email'],
            "name": json_data["full_name"],
            "title": f"Your enquiry has been sent!",
            'trader_details': get_company_details,
            'template': 'enquiry'
        })

        return output

    else:
        #TODO error is returned with a 200 status code
        return jsonify({'error': '403', 'error_message': 'company_id is not valid'})

@enquiry.route('/generate_presigned_url', methods=['POST'])
def generate_presigned_url():
    json_data = request.json
    #replace this..
    # do a check that company id is in account_api
    check_company_bool = AccountApi().get_company(json_data.get('company_id'))
    if check_company_bool != False:
    
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
            presigned_url = s3_client_limted.generate_presigned_url('put_object',
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
    return result_dict
