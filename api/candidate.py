from flask import Blueprint, jsonify

from .data import data_candidate

api_candidate = Blueprint("candidate", __name__)


@api_candidate.route("/", methods=["GET"])
def get_candidate() -> dict:
    """
    Get candidate data
    Returns:
        dict: Candidate data
    """
    return jsonify(data_candidate)
