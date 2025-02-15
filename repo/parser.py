import io
from typing import Dict, List

import pandas as pd


class RepoParser:
    @classmethod
    def parse_plataforms(cls, response: List) -> List:
        """
            Extraindo so o campo value das plataforma
        Args:
            response (_type_): Lista com o text e value das plataforma

        Returns:
            List: Lista com os nomes das plataformas
        """
        platforms = list()
        for i in response:
            platforms.append(i["value"])

        return platforms

    @classmethod
    def parse_plataforms_fields(cls, fields: List) -> str:
        """
            Tranformando so fields que estão em uma lista em str
        Args:
            fields (List): List de dict com os fields

        Returns:
            str: fields em uma unica string
        """
        platforms_field = ",".join(field["value"] for field in fields)
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
        """
            Gerando dataframe com os dados do insights
        Args:
            data_insights (_type_): Lista com os dados do insights
            accounts (_type_): Dict com os id name das contas
        Returns:
            Dataframe: Dataframe com os dados
        """
        map_id = self.__parse_maps_id_name(accounts)

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
        """
            Cria o dataframe com todos os dados agrupados pela plataforma, somando os campos
            numericos
        Args:
            data_insights (_type_): Lista com os dados do insights
            accounts (_type_): Dict com os id name das contas
            plataforma (str): nome da plataforma
            types (str): name ou plataforma

        Returns:
            Dataframe: Dataframe com os dados
        """

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
        agg_data.update({col: lambda _: "" for col in text_cols})

        # Agrupar e consolidar os dados
        df_colap = df_insights.groupby(types).agg(agg_data).reset_index()

        output = io.StringIO()
        df_colap.to_csv(output, index=False)
        return output

    @classmethod
    def parse_data_insights_overview(self, data_insights, accounts):
        """
            Cria o dataframe com todos os dados agrupados pela plataforma, somando os campos
            numericos
        Args:
            data_insights (_type_): Lista com os dados do insights
            accounts (_type_): Dict com os id name das contas

        Returns:
            Dataframe: Dataframe com os dados
        """
        map_id = self.__parse_maps_id_name(accounts)
        types = ["plataforma"]
        for i in data_insights:
            i["name"] = map_id.get(i["id"], "")

        df_insights = self.__create_dataframe(data_insights)

        # Identificar colunas numéricas e de texto
        numeric_cols = df_insights.select_dtypes(include=["number"]).columns.tolist()

        text_cols = [
            col
            for col in df_insights.columns
            if col not in numeric_cols and col not in types  # "name"
        ]

        # Criar regras de agregação dinamicamente,para caso em que as
        # colunas não são fixas
        agg_data = {col: "sum" for col in numeric_cols}

        agg_data.update({col: lambda _: "" for col in text_cols})

        # Agrupar e consolidar os dados
        df_colap = df_insights.groupby(types).agg(agg_data).reset_index()

        output = io.StringIO()
        df_colap.to_csv(output, index=False)
        return output

    @classmethod
    def parse_add_key_dict(self, dt_geral: List, plataforma: str) -> List:
        """
            Adicionando campo plataforma no dados gerais
        Args:
            dt_geral (List): Lista com todos os dados
            plataforma (str): nome da plataforma

        Returns:
            List: Lista com os dados atualizados
        """
        for i in dt_geral:
            i["plataforma"] = plataforma
        return dt_geral

    def __parse_maps_id_name(accounts: List) -> Dict:
        """
            Estruturando melhor os dados com id e name
        Args:
            accounts (List): Lista com os dados das contas

        Returns:
            Dict: Dict com o id e name
        """
        map_id = {int(key["id"]): key["name"] for key in accounts}
        return map_id

    def __create_dataframe(data: List) -> pd.DataFrame:
        """
            Criando o dataframe com os dados
        Args:
            data (List): Lista com os dados

        Returns:
            Dataframe: Dataframe gerado  com os dados
        """
        return pd.DataFrame(data)
