import io

import pandas as pd


class RepoParser:
    @classmethod
    def parse_plataforms(cls, response):
        platforms = list()
        for i in response:
            platforms.append(i["value"])
        # platforms = [platforms["value"] for platforms in response["platforms"]]
        return platforms

    @classmethod
    def parse_plataforms_fields(cls, fields):
        print(fields)
        platforms_field = ",".join(field["value"] for field in fields)
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
            for i in data_accounts
        ]
        return d_accounts

    @classmethod
    def parse_data_insights(self, data_insights, accounts, plataforma):
        map_id = self.__parse_maps_id_name(accounts)

        for i in data_insights:
            i["name"] = map_id.get(i["id"], "")
            i["plataforma"] = plataforma
            i.pop("id")

        df = pd.DataFrame(data_insights)
        output = io.StringIO()
        df.to_csv(output, index=False)

        return output

    @classmethod
    def parse_data_insights_resumo(self, data_insights, accounts, plataforma):
        map_id = self.__parse_maps_id_name(accounts)

        for i in data_insights:
            i["name"] = map_id.get(i["id"], "")
            i["plataforma"] = plataforma

        df_insights = self.__create_dataframe(data_insights)

        # Definir colunas numéricas para soma
        numeric_cols = ["clicks", "cost", "impressions"]

        # Agrupar por nome da conta e consolidar os dados
        df_colap = (
            df_insights.groupby("plataforma")
            .agg(
                {col: "sum" for col in numeric_cols}  # Soma colunas numéricas
                | {
                    "ad_name": lambda _: "",
                    "country": lambda _: "",
                    "status": lambda _: "",
                }
            )
            .reset_index()
        )
        output = io.StringIO()
        df_colap.to_csv(output, index=False)
        return output

    def __parse_maps_id_name(accounts):
        map_id = {int(key["id"]): key["name"] for key in accounts}
        return map_id

    def __create_dataframe(data):
        return pd.DataFrame(data)
