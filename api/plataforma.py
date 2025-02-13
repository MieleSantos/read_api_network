from flask import Blueprint, jsonify, Response
from core.plataforms_api import plataforms_client
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
    fields = plataforms_client.get_platform_fields(plataforma)
    fields_parser = RepoParser.parse_plataforms_fields(fields)

    accounts = plataforms_client.get_accounts(plataforma)
    data_accounts = RepoParser.parse_data_accounts(accounts["body"])

    data = []
    for acc in data_accounts:
        insa = plataforms_client.get_platform_insights(
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


@api_plataforma.route("/<string:plataforma>/resumo", methods=["GET"])
def get_platforms_resumo(plataforma): ...


@api_plataforma.route("/geral", methods=["GET"])
def get_platforms_geral(): ...


@api_plataforma.route("/geral/resumo", methods=["GET"])
def get_resumo_platforms_geral(): ...
