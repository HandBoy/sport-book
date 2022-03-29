from flask import Flask
from flask_restful import Api
from .ext import database, serializer, swagger
from . import configuration
from app.api import sports, pets

from os import environ
from flask_apispec import FlaskApiSpec


def create_app(config_name=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    env = environ.get("FLASK_ENV")
    app.config.from_object(configuration.config_by_name[env])
    api = Api(app)

    database.init_app(app)
    serializer.init_app(app)
    swagger.init_app(app)

    api.add_resource(sports.SportsView, "/api/v1/sports")
    api.add_resource(pets.PetResource, "/api/pet")

    docs = FlaskApiSpec(app)
    docs.register(sports.SportsView)
    docs.register(pets.PetResource)

    return app
