from datetime import datetime

import pytest
from slugify import slugify

from app import create_app
from app.domain import Event, EventStatus, EventType, Outcome, Selection, Sport
from app.repositories.event_repository import EventRepository
from app.repositories.selection_repository import SelectionRepository
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
        Sport(
            id=1,
            slug="teste-01",
            active=True,
        ),
    )
    return result


@pytest.fixture()
def create_event(create_sport):
    repository = EventRepository()

    name = "Event Name"
    event = Event(
        sport_id=create_sport.id,
        name=name,
        slug=slugify(name),
        active=True,
        event_type=EventType.preplay,
        status=EventStatus.pending,
        scheduled_at=datetime.utcnow(),
        start_at=datetime.utcnow(),
    )
    repository.create_event(event)
    return repository.get_event_by_uuid(event.uuid)


@pytest.fixture()
def make_raw_event(create_sport):
    name = "Updated Event"
    return {
        "sport_uuid": create_sport.uuid,
        "name": name,
        "active": True,
        "event_type": EventType.preplay.value,
        "status": EventStatus.pending.value,
        "scheduled_at": datetime.utcnow().isoformat(),
        "start_at": datetime.utcnow().isoformat(),
    }


@pytest.fixture()
def create_selection(create_event):
    repository = SelectionRepository()
    selection = Selection(
        event_id=create_event.id,
        price=10.5,
        active=True,
        outcome=Outcome.unsettled.value,
    )
    repository.create_selection(selection)

    return repository.get_selection_by_uuid(selection.uuid)


@pytest.fixture()
def make_raw_selection(create_event):
    return {
        "event_uuid": create_event.uuid,
        "price": 50.75,
        "active": True,
        "outcome": Outcome.unsettled.value,
    }
