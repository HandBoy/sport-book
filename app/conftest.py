from os import environ

import pytest
from flask import Flask
from flask_restful import Api

from app import configuration
from app.domain import Sport
from app.repositories import SportRepository

from .api import sports
from .ext import database, serializer


@pytest.fixture()
def mock_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "mock-secret-key")
    monkeypatch.setenv("FLASK_ENV", "testing")
    monkeypatch.setenv("DATABASE_URL", ":memory:")
    monkeypatch.setenv("TOKEN_EXPIRES", "50")


@pytest.fixture()
def app(mock_env):
    app = Flask(__name__, instance_relative_config=True)
    env = environ.get("FLASK_ENV")

    with app.app_context():
        app.config.from_object(configuration.config_by_name[env])
        database.init_app(app)
        database.init_db()
        serializer.init_app(app)

        api = Api(app)

        api.add_resource(sports.SportsView, "/api/v1/sports")
        yield app


@pytest.fixture()
def create_sport():
    repository = SportRepository()
    repository.create_sport(
        Sport(
            id=1,
            slug="teste-01",
            active=True,
        ).dict()
    )
