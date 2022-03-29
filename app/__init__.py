import os

from flask import Flask
from .ext import database
from . import auth, blog, configuration
from . import blog

from os import environ


def create_app(config_name=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    env = environ.get("FLASK_ENV")
    app.config.from_object(configuration.config_by_name[env])

    database.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
