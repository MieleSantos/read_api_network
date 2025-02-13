import os

import requests
from dotenv import load_dotenv

#   - /api/platforms
#    - /api/accounts?platform={{platform}}
#    - /api/fields?platform={{platform}}
#    - /api/insights?platform={{platform}}&account={{account}}&token={{token}}&fields={{field1,field2,etc}}


class UrlBase:
    @classmethod
    def get_url(self):
        load_dotenv()

        if not os.getenv("URL_BASE") or not os.getenv("TOKEN"):
            raise ValueError("URL_BASE or TOKEN not found")

        url = os.getenv("URL_BASE")

        headers = {
            "Authorization": f"Bearer {os.getenv('TOKEN')}",
            "Content-Type": "application/json",
        }

        return url, headers


class PlataformsClient:
    def __init__(self):
        self.url, self.headers = UrlBase.get_url()

    def __check_response(self, response):
        if response.status_code == 200:
            return {"status_code": 200, "body": response.json()}
        else:
            return {
                "status_code": response.status_code,
                "body": response.raise_for_status(),
            }

    def get_platforms(self):
        response = requests.get(f"{self.url}/platforms", headers=self.headers)
        return self.__check_response(response)

    def get_accounts(self, plataforma):
        response = requests.get(
            f"{self.url}/accounts?platform={plataforma}", headers=self.headers
        )
        return self.__check_response(response)

    def get_platform_fields(self, plataforma):
        response = requests.get(
            f"{self.url}/fields?platform={plataforma}", headers=self.headers
        )
        return self.__check_response(response)

    def get_platform_insights(self, plataforma, account, token, fields):
        response = requests.get(
            f"{self.url}/insights?platform={plataforma}&account={account}&token={token}&fields={fields}",
            headers=self.headers,
        )
        return self.__check_response(response)


plataforms_client = PlataformsClient()
