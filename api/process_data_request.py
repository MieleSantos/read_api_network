from typing import Tuple

from core.plataforms_api import plataforms_client
from repo.parser import RepoParser


platform_map = {  # noqa: F811
    "meta_ads": "Facebook Ads",
    "ga4": "Google Analytics",
    "tiktok_insights": "TikTok",
}


def preparation_request_platform(plataforma: str):
    """
        Prepara as requisições que para serem feitas para os endpoints
        retornando os dados em dataframe
    Returns:
        Tuple: Tupla com os dados para monta o relatorio
    """
    fields = plataforms_client.get_platform_fields(plataforma)
    fields_parser = RepoParser.parse_plataforms_fields(fields)

    data_accounts = plataforms_client.get_accounts(plataforma)

    data = []
    for dt_acc in data_accounts:
        dt_insights = plataforms_client.get_platform_insights(
            plataforma,
            dt_acc["id"],
            dt_acc["token"],
            fields_parser,
        )
        data.extend(dt_insights)
    return data


def preparation_request_all() -> Tuple:
    """
        Prepara as requisições que para serem feitas para os endpoints
        retornando os dados em dataframe
    Returns:
        Tuple: Tupla com os dados para monta o relatorio
    """
    data_geral = []
    data_accounts = []
    fields = []
    fields_parser = []

    plataforms = plataforms_client.get_plataform()
    list_plataforms = RepoParser.parse_plataforms(plataforms)

    for plataforma in list_plataforms:
        fields.extend(plataforms_client.get_platform_fields(plataforma))
        dt_accounts = plataforms_client.get_accounts(plataforma)
        dt_accounts = RepoParser.parse_add_key_dict(dt_accounts, plataforma)
        data_accounts.extend(dt_accounts)

        fields_parser = RepoParser.parse_plataforms_fields(fields)

        for dt_acc in data_accounts:
            # requisição para pega os insights
            dt_insights = plataforms_client.get_platform_insights(
                plataforma,
                dt_acc["id"],
                dt_acc["token"],
                fields_parser,
            )
            dt_insights = RepoParser.parse_add_key_dict(dt_insights, plataforma)

            data_geral.extend(dt_insights)
    return data_geral, data_accounts, plataforma
