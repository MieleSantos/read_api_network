from flask import Blueprint, Response
from repo.parser import RepoParser

api_candidate = Blueprint("candidate", __name__)


@api_candidate.route("/", methods=["GET"])
def get_candidate():
    """
    Get candidate data
    Returns:
        dict: Candidate data
    """
    resp = RepoParser.parse_data_candidate()

    response = Response(resp.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=candidate.csv"

    return response
