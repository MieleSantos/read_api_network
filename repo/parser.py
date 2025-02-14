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
        print(data_insights)
        for i in data_insights:
            i["name"] = map_id.get(i["id"], "")
            # i["plataforma"] = plataforma
            i.pop("id")

        df = pd.DataFrame(data_insights)
        output = io.StringIO()
        df.to_csv(output, index=False)

        return output

    @classmethod
    def parse_data_insights_resumo(self, data_insights, accounts, plataforma, types):
        map_id = self.__parse_maps_id_name(accounts)

        for i in data_insights:
            i["name"] = map_id.get(i["id"], "")
            i["plataforma"] = plataforma

        df_insights = self.__create_dataframe(data_insights)

        # Identificar colunas numéricas e de texto
        numeric_cols = df_insights.select_dtypes(include=["number"]).columns.tolist()
        text_cols = [
            col
            for col in df_insights.columns
            if col not in numeric_cols and col != types  # "name"
        ]

        # Criar regras de agregação dinamicamente
        agg_data = {col: "sum" for col in numeric_cols}  # Soma para colunas numéricas
        agg_data.update(
            {col: lambda _: "" for col in text_cols}
        )  # Campos de texto vazios

        # Agrupar e consolidar os dados
        df_colap = df_insights.groupby(types).agg(agg_data).reset_index()

        output = io.StringIO()
        df_colap.to_csv(output, index=False)
        return output

    @classmethod
    def parse_data_insights_all(self, data_insights, accounts, plataforma):
        map_id = self.__parse_maps_id_name(accounts)
        types = ["name", "plataforma"]
        for i in data_insights:
            i["name"] = map_id.get(i["id"], "")
        # i["plataforma"] = plataforma
        print(data_insights)
        df_insights = self.__create_dataframe(data_insights)

        # Identificar colunas numéricas e de texto
        numeric_cols = df_insights.select_dtypes(include=["number"]).columns.tolist()
        text_cols = [
            col
            for col in df_insights.columns
            if col not in numeric_cols and col not in types  # "name"
        ]

        # Criar regras de agregação dinamicamente
        agg_data = {col: "sum" for col in numeric_cols}
        # agg_data.update(
        #     {"name": "first", "plataforma": "first"}
        # )  # Mantém o primeiro valor para nome e plataforma# Soma para colunas numéricas
        agg_data.update(
            {col: lambda _: "" for col in text_cols}
        )  # Campos de texto vazios
        print(df_insights.head())

        # Agrupar e consolidar os dados
        df_colap = df_insights.groupby(types).agg(agg_data).reset_index()

        output = io.StringIO()
        df_colap.to_csv(output, index=False)
        return output

    def __parse_maps_id_name(accounts):
        map_id = {int(key["id"]): key["name"] for key in accounts}
        return map_id

    def __create_dataframe(data):
        return pd.DataFrame(data)
