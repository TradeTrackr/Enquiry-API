from tabnanny import check
from flask import Flask, request, jsonify
from functools import wraps
from enquiry_api.dependencies.account_api import AccountApi


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
            check_token = AccountApi().check_token({"access_token": token})
            if check_token.get('valid_token') is not True:
                return jsonify({'error': 'Invalid token'}), 403
        else:
            return jsonify({'error': 'Authorization header missing or invalid'}), 403

        return f(*args, **kwargs)

    return decorated
