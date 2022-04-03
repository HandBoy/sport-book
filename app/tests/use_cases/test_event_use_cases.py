import uuid
from datetime import datetime

import pytest
from app.domain import EventStatus, EventType
from app.repositories.exceptions import (
    EventForeignKeyException,
    EventValidationErrorException,
)
from app.repositories.sport_repository import SportRepository
from app.use_cases.event_use_cases import (
    CreateEventUsecase,
    ListEventUsecase,
    UpdateEventUsecase,
)
from slugify import slugify


class TestListEventsUsecase:
    def test_list_event(self, app, create_event):
        # Give
        use_case = ListEventUsecase()
        # Act
        events = use_case.execute()
        # Them
        assert len(events) == 5

    def test_get_events_by_slug(self, app, create_event):
        # Give
        filters = {"slug": create_event.slug}
        use_case = ListEventUsecase()
        # Act
        events = use_case.execute(filters)
        # Them
        assert events != None
        assert len(events) == 1

    def test_get_events_by_slug_and_active(self, app, create_event):
        # Give
        filters = {"slug": create_event.slug, "active": create_event.active}
        use_case = ListEventUsecase()
        # Act
        events = use_case.execute(filters)
        # Them
        assert events != None
        assert len(events) == 1

    def test_get_events_by_slug_and_active_false(self, app, create_event):
        # Give
        filters = {"slug": create_event.slug, "active": False}
        use_case = ListEventUsecase()
        # Act
        sports = use_case.execute(filters)
        # Them
        assert sports != None
        assert len(sports) == 0


class TestCreateEventUsecase:
    def test_create_event(self, app, create_sport):
        # Give
        use_case = CreateEventUsecase()
        name = "Event Name"
        data = {
            "sport_uuid": create_sport.uuid,
            "name": name,
            "slug": slugify(name),
            "active": True,
            "event_type": EventType.preplay,
            "status": EventStatus.pending,
            "scheduled_at": datetime.now(),
            "start_at": datetime.now(),
        }
        # Act
        event = use_case.execute(data)
        # Them
        assert event != None

    def test_create_event_without_slug(self, app, create_sport):
        # Give
        use_case = CreateEventUsecase()
        data = {"sport_uuid": create_sport.uuid, "active": True}
        # Act
        # Them
        with pytest.raises(EventValidationErrorException):
            use_case.execute(data)

    def test_create_event_without_nonexistent_sport(self, app, create_sport):
        # Give
        use_case = CreateEventUsecase()
        name = "Event Name"
        data = {
            "sport_uuid": uuid.uuid4(),
            "name": name,
            "slug": slugify(name),
            "active": True,
            "event_type": EventType.preplay,
            "status": EventStatus.pending,
            "scheduled_at": datetime.now(),
            "start_at": datetime.now(),
        }
        # Act
        # Them
        with pytest.raises(EventForeignKeyException):
            use_case.execute(data)


class TestInactivateEventUseCase:
    def test_inactivate_all_events(self, app, create_event):
        # Give
        sport = SportRepository().get_sport_by_id(create_event.sport_id)
        data = {
            "sport_uuid": sport.uuid,
            "name": "New Event",
            "active": False,
            "event_type": EventType.preplay.value,
            "status": EventStatus.pending.value,
            "scheduled_at": datetime.utcnow().isoformat(),
            "start_at": datetime.utcnow().isoformat(),
        }
        # Act
        UpdateEventUsecase().execute(create_event.uuid, data)
        # Them
        sport = SportRepository().get_sport_by_id(create_event.sport_id)
        assert sport.active == False
