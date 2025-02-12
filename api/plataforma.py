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


@api_plataforma.route("/plataforma", methods=["GET"])
def get_platforms():
    response = PlataformsClient.get_platforms()
    # print(response)
    if response["status_code"] == 200:
        plataformas = RepoParser.parse_plataforms(response["body"])
        # print(plataformas)

        for plataforma in plataformas[:1]:
            fields = PlataformsClient.get_platform_fields(plataforma)
            # print(fields)
            accounts = PlataformsClient.get_accounts(plataforma)
            # print(accounts)
            data_accounts = RepoParser.parse_data_accounts(accounts["body"])
            print(data_accounts)
            for acc in data_accounts:
                insa = PlataformsClient.get_platform_insights(
                    plataforma,
                    acc["id"],
                    acc["token"],
                    fields,
                )
                print(insa)
            # accounts = RepoParser

    else:
        return jsonify(response["body"])
    # return jsonify(response)
