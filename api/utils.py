from flask import Response, jsonify


from core.plataforms_api import plataforms_client
from repo.parser import RepoParser


platform_map = {  # noqa: F811
    "meta_ads": "Facebook Ads",
    "ga4": "Google Analytics",
    "tiktok_insights": "TikTok",
}


def add_key_dict(dt_geral, plataforma):
    for i in dt_geral:
        i["plataforma"] = plataforma
    return dt_geral


def process_req():
    data_geral = []
    data_accounts = []
    fields = []
    fields_parser = []
    plataforms = plataforms_client.get_plataform()
    list_plataforms = RepoParser.parse_plataforms(plataforms)

    for plataforma in list_plataforms:
        fields.extend(plataforms_client.get_platform_fields(plataforma))
        dt_accounts = plataforms_client.get_accounts(plataforma)
        dt_accounts = add_key_dict(dt_accounts, plataforma)
        data_accounts.extend(dt_accounts)

        fields_parser = RepoParser.parse_plataforms_fields(fields)

        for acc in data_accounts:
            dt_insights = plataforms_client.get_platform_insights(
                plataforma,
                acc["id"],
                acc["token"],
                fields_parser,
            )
            dt_insights = add_key_dict(dt_insights, plataforma)

            data_geral.extend(dt_insights)
    # output = RepoParser.parse_data_insights_all(
    #     data_geral, data_accounts, platform_map[plataforma]
    # )
    # response = Response(output.getvalue(), mimetype="text/csv")
    # response.headers["Content-Disposition"] = "attachment; filename=insights_geral.csv"
    return data_geral, data_accounts, plataforma

    #     accounts = plataforms_client.get_accounts(plataforma)
    #     data_accounts = RepoParser.parse_data_accounts(accounts)

    #     for acc in data_accounts:
    #         insa = plataforms_client.get_platform_insights(
    #             plataforma,
    #             acc["id"],
    #             acc["token"],
    #             fields_parser,
    #         )
    #         data.extend(insa)
    #     print(plataforma)
    #     output = RepoParser.parse_data_insights_resumo(
    #         data, data_accounts, platform_map[plataforma], types
    #     )
    # response = Response(output.getvalue(), mimetype="text/csv")
    # response.headers["Content-Disposition"] = "attachment; filename=insights_geral.csv"
    # return response
