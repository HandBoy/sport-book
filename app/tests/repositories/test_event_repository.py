from datetime import datetime

import pytest
from app.domain import Event, EventStatus, EventType
from app.repositories.event_repository import EventRepository
from app.repositories.exceptions import RepositoryOperationalError
from slugify import slugify


class TestGetEventRepository:
    def test_get_events(self, app):
        # Give
        repository = EventRepository()
        # Act
        events = repository.get_events()
        # Them
        assert events != None
        assert len(events) == 4

    def test_get_event_by_name(self, app):
        # Give
        filters = {"name": "Event First"}
        repository = EventRepository()
        # Act
        events = repository.get_events(filters)
        # Them
        assert events != None
        assert len(events) == 1
        assert events[0].name == filters["name"]

    def test_get_event_by_slug(self, app):
        # Give
        filters = {"slug": "event-first"}
        repository = EventRepository()
        # Act
        events = repository.get_events(filters)
        # Them
        assert events != None
        assert len(events) == 1
        assert events[0].slug == filters["slug"]

    def test_get_events_by_slug_and_active(self, app):
        # Give
        filters = {"slug": "event-second", "active": 0}
        repository = EventRepository()
        # Act
        events = repository.get_events(filters)
        # Them
        assert events != None
        assert len(events) == 1
        assert events[0].slug == filters["slug"]

    def test_get_unexistent_events_by_slug(self, app):
        # Give
        filters = {"slug": "foo-bar"}
        repository = EventRepository()
        # Act
        events = repository.get_events(filters)
        # Them
        assert events != None
        assert len(events) == 0

    def test_get_all_active_events(self, app):
        # Give
        filters = {"active": 1}
        repository = EventRepository()
        # Act
        events = repository.get_events(filters)
        # Them
        assert events != None
        assert len(events) == 2

    def test_get_events_by_unexistent_filter(self, app):
        # Give
        filters = {"filter": "foo-bar"}
        repository = EventRepository()
        # Act
        # Them
        with pytest.raises(RepositoryOperationalError):
            repository.get_events(filters)


class TestCreateEventRepository:
    def test_create_event(self, app, create_sport):
        # Give
        name = "Event name"
        expected_event = Event(
            sport_id=create_sport.id,
            name=name,
            slug=slugify(name),
            active=True,
            event_type=EventType.preplay,
            status=EventStatus.pending,
            scheduled_at=datetime.now(),
            start_at=datetime.now(),
        )
        repository = EventRepository()
        # Act
        repository.create_event(expected_event)
        event = repository.get_event_by_uuid(expected_event.uuid)
        # Them
        assert event.name == expected_event.name
        assert event.slug == expected_event.slug
        assert event.status == expected_event.status
