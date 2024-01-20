import json
import requests
from flask import current_app, g, request, session
from enquiry_api import config

class AccountApi(object):

    def get_company(self, id):

        headers = {
            "Content-Type": "application/json",
        }

        resp = requests.get(
            config.ACCOUNT_API_ENDPOINT + f"/trader/check_trader/{id}",
            headers=headers,
        )

        return json.loads(resp.text)

    def check_token(self, params):

        headers = {
            "Content-Type": "application/json",
        }

        resp = requests.get(
            config.ACCOUNT_API_ENDPOINT + f"/auth/check_token",
            headers=headers,
            data=json.dumps(params)

        )

        return json.loads(resp.text)
