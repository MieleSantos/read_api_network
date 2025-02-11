from flask import Blueprint, jsonify
from core.plataforms_api import PlataformsClient
from repo.parser import RepoParser
# TODO implementar essas rotas
# /  nome, email e o link para o seu LinkedIn (se tiver).
# /{{plataforma}}
# /{{plataforma}}/resumo
# /geral
# /geral/resumo

api_plataforma = Blueprint("plataforma", __name__)


@api_plataforma.route("/platforms", methods=["GET"])
def get_platamorms():
    response = PlataformsClient.get_platforms()
    if response["status_code"] == 200:
        RepoParser.parse_plataforms(response["body"])
    else:
        return jsonify(response["body"])
    # return jsonify(response)
