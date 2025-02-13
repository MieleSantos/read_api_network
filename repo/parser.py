import io

import pandas as pd


class RepoParser:
    @classmethod
    def parse_plataforms(cls, response):
        platforms = list()
        for i in response["platforms"]:
            platforms.append(i["value"])
        # platforms = [platforms["value"] for platforms in response["platforms"]]
        return platforms

    @classmethod
    def parse_plataforms_fields(cls, fields):
        print(fields)
        platforms_field = ",".join(field["value"] for field in fields["body"]["fields"])
        # for i in fields["fields"]:
        #     platforms.append(i["value"])
        return platforms_field

    @classmethod
    def parse_data_candidate(cls):
        data_candidate = [
            {
                "name": "Miele Silva",
                "email": "mielesnts@gmail.com",
                "linkedin": "https://www.linkedin.com/in/mielesilva/",
            }
        ]

        df = pd.DataFrame(data_candidate)
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output

    @classmethod
    def parse_data_accounts(cls, data_accounts):
        d_accounts = [
            {"id": int(i["id"]), "name": i["name"], "token": i["token"]}
            for i in data_accounts["accounts"]
        ]
        return d_accounts

    @classmethod
    def parse_data_insights(cls, data_insights, accounts, plataforma):
        map_id = cls._parse_maps_id_name(accounts)

        for i in data_insights:
            i["name"] = map_id.get(i["id"], "")
            i["plataforma"] = plataforma

        df = pd.DataFrame(data_insights)
        output = io.StringIO()
        df.to_csv(output, index=False)

        return output

    def _parse_maps_id_name(accounts):
        map_id = {int(key["id"]): key["name"] for key in accounts}
        return map_id


{
    "platforms": [
        {"text": "Facebook Ads", "value": "meta_ads"},
        {"text": "Google Analytics", "value": "ga4"},
        {"text": "TikTok", "value": "tiktok_insights"},
    ]
}

{
    "accounts": [
        {
            "id": "1",
            "name": "Ana Patrícia Ramos",
            "token": "e8e54de67d5e78ed6e876ed87e6d8e74",
        },
        {"id": "2", "name": "Duda Lisboa", "token": "e8e54de67d5563ed6e876ed87e6d8e74"},
    ]
}
