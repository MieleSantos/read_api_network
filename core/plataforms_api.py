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
    @classmethod
    def get_platforms(self):
        url, headers = UrlBase.get_url()

        response = requests.get(f"{url}/platforms", headers=headers)
        if response.status_code == 200:
            return {"status_code": 200, "body": response.json()}
        else:
            return {
                "status_code": response.status_code,
                "body": response.raise_for_status(),
            }

    @classmethod
    def get_accounts(self, plataforma):
        url, headers = UrlBase.get_url()

        response = requests.get(
            f"{url}/accounts?platform={plataforma}", headers=headers
        )
        if response.status_code == 200:
            return {"status_code": 200, "body": response.json()}
        else:
            return {
                "status_code": response.status_code,
                "body": response.raise_for_status(),
            }

    @classmethod
    def get_platform_fields(self, plataforma):
        url, headers = UrlBase.get_url()

        response = requests.get(f"{url}/fields?platform={plataforma}", headers=headers)

        if response.status_code == 200:
            return {"status_code": 200, "body": response.json()}
        else:
            return {
                "status_code": response.status_code,
                "body": response.raise_for_status(),
            }

    @classmethod
    def get_platform_insights(self, plataforma, account, token, fields):
        # print("SSSSSS", plataforma, account, token, fields)
        url, headers = UrlBase.get_url()
        response = requests.get(
            f"{url}/insights?platform={plataforma}&account={account}&token={token}&fields={fields}",
            headers=headers,
        )

        if response.status_code == 200:
            return {"status_code": 200, "body": response.json()}
        else:
            return {
                "status_code": response.status_code,
                "body": response.raise_for_status(),
            }
