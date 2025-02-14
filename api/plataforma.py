from flask import Blueprint, Response, jsonify

from api.utils import platform_map, process_req
from core.plataforms_api import plataforms_client
from repo.parser import RepoParser

api_plataforma = Blueprint("plataforma", __name__)


@api_plataforma.route("/<string:plataforma>", methods=["GET"])
def get_platforms(plataforma):
    fields = plataforms_client.get_platform_fields(plataforma)
    fields_parser = RepoParser.parse_plataforms_fields(fields)

    accounts = plataforms_client.get_accounts(plataforma)
    data_accounts = RepoParser.parse_data_accounts(accounts)

    data = []
    for acc in data_accounts:
        insa = plataforms_client.get_platform_insights(
            plataforma,
            acc["id"],
            acc["token"],
            fields_parser,
        )
        data.extend(insa)
    output = RepoParser.parse_data_insights(
        data, data_accounts, platform_map[plataforma]
    )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights.csv"
    return response


@api_plataforma.route("/<string:plataforma>/resumo", methods=["GET"])
def get_platforms_resumo(plataforma):
    fields = plataforms_client.get_platform_fields(plataforma)
    fields_parser = RepoParser.parse_plataforms_fields(fields)

    accounts = plataforms_client.get_accounts(plataforma)
    data_accounts = RepoParser.parse_data_accounts(accounts)

    data = []
    for acc in data_accounts:
        insa = plataforms_client.get_platform_insights(
            plataforma,
            acc["id"],
            acc["token"],
            fields_parser,
        )
        data.extend(insa)
    types = "name"
    output = RepoParser.parse_data_insights_resumo(
        data, data_accounts, platform_map[plataforma], types
    )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights_resumo.csv"
    return response


@api_plataforma.route("/geral", methods=["GET"])
def get_platforms_geral():
    data_geral, data_accounts, plataforma = process_req()
    output = RepoParser.parse_data_insights(
        data_geral, data_accounts, platform_map[plataforma]
    )
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights_geral.csv"
    return response


@api_plataforma.route("/geral/resumo", methods=["GET"])
def get_resumo_platforms_geral():
    data_geral, data_accounts, plataforma = process_req()
    output = RepoParser.parse_data_insights_all(
        data_geral, data_accounts, platform_map[plataforma]
    )

    # output = RepoParser.parse_data_insights_all(
    #     data_geral, data_accounts, platform_map[plataforma]
    # )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights_geral.csv"
    return response
