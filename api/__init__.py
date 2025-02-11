import os

from flask import Flask
from .candidate import api_candidate
from .plataforma import api_plataforma


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(api_candidate)
    app.register_blueprint(api_plataforma)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app
