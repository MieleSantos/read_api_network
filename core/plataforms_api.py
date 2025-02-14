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

    def get_plataform(self):
        return self._fetch_paginated_data(endpoint="platforms", params=None)

    def _fetch_paginated_data(self, endpoint: str, params):
        all_data = []
        page = 1

        while True:
            response = self._fetch_page(endpoint, params, page)
            if not response:
                break

            all_data.extend(response.get(endpoint, []))

            # Verifica a paginação
            pagination = response.get("pagination", {})
            if pagination.get("current", 1) >= pagination.get("total", 1):
                break

            page += 1

        return all_data

    def _fetch_page(self, endpoint, params, page):
        url = f"{self.url}/{endpoint}"
        params = params or {}

        params["page"] = page

        response = requests.get(url, params=params, timeout=10, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def get_platforms(self):
        return self._fetch_paginated_data(endpoint="platforms", params=None)

    def get_accounts(self, plataforma):
        return self._fetch_paginated_data(
            endpoint="accounts", params={"platform": plataforma}
        )

    def get_platform_fields(self, plataforma):
        return self._fetch_paginated_data(
            endpoint="fields", params={"platform": plataforma}
        )

    def get_platform_insights(self, plataforma, account, token, fields):
        params = {
            "platform": plataforma,
            "account": account,
            "token": token,
            "fields": fields,
        }
        return self._fetch_paginated_data(endpoint="insights", params=params)


plataforms_client = PlataformsClient()
