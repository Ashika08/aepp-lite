# connector.py

from enum import Enum
import config
import requests
import json


class Method(Enum):
    GET = "get"
    PUT = "put"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"
    HEAD = "head"


class Connector:

    def __init__(self, org_id: str, client_id: str, tech_id: str, secret: str, path_to_key: str, sandbox_name: str):
        self.config_data = {
            "org_id": org_id,
            "client_id": client_id,
            "tech_id": tech_id,
            "secret": secret,
            "path_to_key": path_to_key,
            "sandbox_name": sandbox_name
        }
        self.__authenticate()

    def __authenticate(self):
        self.config_data["encoded_jwt_token"] = config.get_encoded_jwt_token(
            self.config_data)
        self.config_data["access_token"] = config.get_access_token(
            self.config_data)

    def call_api(self, method: Method, url: str, headers: dict, query_params: dict, path_variables: dict, body: dict):
        default_header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config_data['access_token']}",
            "x-api-key": self.config_data["client_id"],
            "x-gw-ims-org-id": self.config_data["org_id"],
            "x-sandbox-name": self.config_data["sandbox_name"]
        }

        if headers:
            for header_key, header_value in headers.items():
                default_header[header_key] = header_value

        if path_variables:
            for path_variables_value in path_variables.values():
                url = f'{url}/{path_variables_value}'
        try:
            if method == Method.GET:
                request = requests.get(
                    url=url, headers=default_header, params=query_params)
            elif method == Method.PUT:
                request = requests.put(
                    url=url, headers=default_header, params=query_params, json=body)
            elif method == Method.POST:
                request = requests.post(
                    url=url, headers=default_header, params=query_params, json=body)
            elif method == Method.PATCH:
                request = requests.patch(
                    url=url, headers=default_header, params=query_params, json=body)
            elif method == Method.DELETE:
                request = requests.delete(
                    url=url, headers=default_header, params=query_params, json=body)
            request.raise_for_status()

        except requests.HTTPError as err_http:
            raise requests.HTTPError("Http Error:", err_http)
        except requests.ConnectionError as err_conn:
            raise requests.ConnectionError("Connection Error:", err_conn)
        except requests.RequestException as err:
            raise requests.RequestException(
                f"Error while trying to access {url}", err)

        response = request.json()
        pretty_response = json.dumps(response, indent=4)

        # print(url)
        print(pretty_response)
