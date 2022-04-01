import pytest

from app import create_app
from app.domain import Sport
from app.repositories.sport_repository import SportRepository

from .ext import database


@pytest.fixture()
def mock_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "mock-secret-key")
    monkeypatch.setenv("FLASK_ENV", "testing")
    monkeypatch.setenv("DATABASE_URL", ":memory:")
    monkeypatch.setenv("TOKEN_EXPIRES", "50")


@pytest.fixture()
def app(mock_env):
    app = create_app()

    with app.app_context():        
        database.init_db()
        yield app


@pytest.fixture()
def create_sport():
    repository = SportRepository()
    result = repository.create_sport(
        Sport(id=1, slug="teste-01", active=True),
    )
    return result
