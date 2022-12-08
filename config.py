# config.py

import constants
import datetime
import json
import jwt
import requests


class Config:

    def __init__(self):
        with open('credentials.json', 'r') as config_file:
            config_data = json.load(config_file)
        self.org_id = config_data['credentials']['org_id']
        self.client_id = config_data['credentials']['client_id']
        self.tech_id = config_data['credentials']['tech_id']
        self.secret = config_data['credentials']['secret']
        self.path_to_key = config_data['credentials']['pathToKey']
        self.sandbox_name = config_data['credentials']['sandbox-name']
        self.encoded_jwt_token = self.get_encoded_jwt_token()
        self.access_token = self.get_access_token()

    def get_encoded_jwt_token(self) -> str:
        # token expires after 5 minutes
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=300)

        private_key_path = self.path_to_key
        with open(private_key_path, 'r') as private_key_file:
            private_key = private_key_file.read()

        self.jwt_token = {
            "exp": expiry_time,
            "iss": self.org_id,
            "sub": self.tech_id,
            "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
            "aud": f"https://ims-na1.adobelogin.com/c/{self.client_id}"
        }
        encoded_jwt_token = jwt.encode(
            self.jwt_token, private_key, algorithm="RS256")
        return encoded_jwt_token

    def get_access_token(self):
        access_token_payload = {
            "client_id": self.client_id,
            "client_secret": self.secret,
            "jwt_token": self.encoded_jwt_token,
        }

        jwt_token_endpoint = constants.JWT_TOKEN_ENDPOINT
        jwt_token_request = requests.post(
            url=jwt_token_endpoint, data=access_token_payload)
        jwt_token_response = jwt_token_request.json()
        access_token = jwt_token_response['access_token']

        return access_token
