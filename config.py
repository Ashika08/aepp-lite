# config.py

import constants
import datetime
import json
import jwt
import requests


def get_encoded_jwt_token(credentials: dict) -> str:
    # token expires after 5 minutes
    expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=300)

    private_key_path = credentials["path_to_key"]
    with open(private_key_path, 'r') as private_key_file:
        private_key = private_key_file.read()

    jwt_token = {
        "exp": expiry_time,
        "iss": credentials["org_id"],
        "sub": credentials["tech_id"],
        "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
        "aud": f"https://ims-na1.adobelogin.com/c/{credentials['client_id']}"
    }
    encoded_jwt_token = jwt.encode(
        jwt_token, private_key, algorithm="RS256")
    return encoded_jwt_token


def get_access_token(credentials: dict) -> str:
    access_token_payload = {
        "client_id": credentials["client_id"],
        "client_secret": credentials["secret"],
        "jwt_token": credentials["encoded_jwt_token"],
    }

    jwt_token_endpoint = constants.JWT_TOKEN_ENDPOINT
    jwt_token_request = requests.post(
        url=jwt_token_endpoint, data=access_token_payload)
    jwt_token_response = jwt_token_request.json()
    access_token = jwt_token_response['access_token']

    return access_token
