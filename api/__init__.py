# import os

from flask import Flask
from .candidate import api_candidate
from .plataforma import api_plataforma


def create_app():
    """_summary_

    Returns:
        _type_: _description_
    """
    app = Flask(__name__)
    app.register_blueprint(api_candidate)
    app.register_blueprint(api_plataforma)

    return app
