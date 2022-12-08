# connector.py

import config
import constants
import requests


class Connect:

    def __init__(self):
        self.config_data = config.Config()
        print(self.config_data.access_token)

    def call_api(self):
        get_datasets_endpoint = f'{constants.DATASET_ENDPOINT}/634d2969f84e311c07e7f27d/labels'
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config_data.access_token}",
            "x-api-key": self.config_data.client_id,
            "x-gw-ims-org-id": self.config_data.org_id,
            "x-sandbox-name": self.config_data.sandbox_name
        }
        get_datasets_params = {
            "DATASET_ID": "634d2969f84e311c07e7f27d"
        }
        get_datasets_request = requests.get(
            url=get_datasets_endpoint, params=get_datasets_params, headers=headers)

        print(get_datasets_request.json())
