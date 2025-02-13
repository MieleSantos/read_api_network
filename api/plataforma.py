from flask import Blueprint, jsonify, Response
from core.plataforms_api import PlataformsClient
from repo.parser import RepoParser
from api.utils import platform_map
# TODO implementar essas rotas
# /  nome, email e o link para o seu LinkedIn (se tiver).
# /{{plataforma}}
# /{{plataforma}}/resumo
# /geral
# /geral/resumo

api_plataforma = Blueprint("plataforma", __name__)


@api_plataforma.route("/<string:plataforma>", methods=["GET"])
def get_platforms(plataforma):
    # response = PlataformsClient.get_platforms()

    # if response["status_code"] == 200:
    # plataformas = RepoParser.parse_plataforms(response["body"])

    # for plataforma in plataformas[:1]:
    # As colunas devem trazer todos os campos de insights daquele anúncio,
    # nome da conta que o está veiculando. Em nenhuma das tabelas precisam ser retornados IDs,
    # Platform,Ad Name,Clicks,...

    #      "value": "meta_ads"
    #      "value": "ga4"

    #     "value": "tiktok_insights"

    fields = PlataformsClient.get_platform_fields(plataforma)
    fields_parser = RepoParser.parse_plataforms_fields(fields)

    accounts = PlataformsClient.get_accounts(plataforma)
    data_accounts = RepoParser.parse_data_accounts(accounts["body"])

    data = []
    for acc in data_accounts:
        insa = PlataformsClient.get_platform_insights(
            plataforma,
            acc["id"],
            acc["token"],
            fields_parser,
        )
        data.extend(insa["body"]["insights"])
    output = RepoParser.parse_data_insights(
        data, data_accounts, platform_map[plataforma]
    )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights.csv"
    return response
