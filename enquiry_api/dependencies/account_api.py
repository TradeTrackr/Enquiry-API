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
            config.ENQUIRY_API_ENDPOINT + f"/trader/check_trader_bool/{id}",
            headers=headers,
        )

        return json.loads(resp.text)