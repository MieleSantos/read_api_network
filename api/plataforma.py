from flask import Blueprint, Response

from api.process_data_request import (
    platform_map,
    preparation_request_all,
    preparation_request_platform,
)

from repo.parser import RepoParser

api_plataforma = Blueprint("plataforma", __name__)


@api_plataforma.route("/<string:plataforma>", methods=["GET"])
def get_platforms(plataforma):
    """
        Endpoint para fazer o resumo dos dados os anuncios
    Args:
        plataforma (str): plataforma de anuncio

    Returns:
        csv: Relatorio em formato de tabelas
    """
    data, data_accounts = preparation_request_platform(plataforma)

    output = RepoParser.parse_data_insights(
        data, data_accounts, platform_map[plataforma]
    )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights.csv"
    return response


@api_plataforma.route("/<string:plataforma>/resumo", methods=["GET"])
def get_platforms_resumo(plataforma):
    """
        Endpoint para fazer o resumo dos dados os anuncios
    Args:
        plataforma (str): plataforma de anuncio

    Returns:
        csv: Relatorio em formato de tabelas
    """
    data, data_accounts = preparation_request_platform(plataforma)

    types = "name"
    output = RepoParser.parse_data_insights_resumo(
        data, data_accounts, platform_map[plataforma], types
    )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights_resumo.csv"
    return response


@api_plataforma.route("/geral", methods=["GET"])
def get_platforms_geral():
    """
        Endpoint para gera o relatorio geral das plataformas
    Returns:
        csv: Relatorio em formato de tabelas
    """
    data_geral, data_accounts, plataforma = preparation_request_all()
    output = RepoParser.parse_data_insights(
        data_geral, data_accounts, platform_map[plataforma]
    )
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights_geral.csv"
    return response


@api_plataforma.route("/geral/resumo", methods=["GET"])
def get_resumo_platforms_geral():
    """
        Endpoint para gera o relatorio geral das plataformas de forma resumida
    Returns:
        csv: Relatorio em formato de tabelas
    """
    data_geral, data_accounts, plataforma = preparation_request_all()
    output = RepoParser.parse_data_insights_overview(
        data_geral, data_accounts, platform_map[plataforma]
    )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=insights_geral.csv"
    return response
