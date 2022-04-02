from os import environ

from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from app.api import exceptions, views

from . import configuration
from .ext import database, serializer


def create_app(config_name=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    env = environ.get("FLASK_ENV")
    app.config.from_object(configuration.config_by_name[env])
    api = Api(app)

    database.init_app(app)
    serializer.init_app(app)
    exceptions.handle_api_exceptions(app)

    api.add_resource(views.SportsListView, "/api/v1/sports")
    api.add_resource(views.SportsView, "/api/v1/sports/<uuid:sport_id>")
    api.add_resource(views.EventListView, "/api/v1/events")

    docs = FlaskApiSpec(app)
    docs.register(views.SportsListView)
    docs.register(views.SportsView)
    docs.register(views.EventListView)

    return app
