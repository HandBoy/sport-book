from typing import Dict, List
from uuid import UUID

from app.repositories.sport_repository import SportRepository
from pydantic import ValidationError

from ..domain import Event
from ..repositories.event_repository import EventRepository
from ..repositories.exceptions import (
    EventForeignKeyException,
    EventValidationErrorException,
    SportNotFoundException,
)


class ListEventUsecase:
    def execute(self, filters: Dict = None) -> List[Event]:
        repo = EventRepository()
        events = repo.get_events(filters)
        return events


class CreateEventUsecase:
    def execute(self, event_raw: Dict) -> Event:
        repository = EventRepository()
        try:
            sport = SportRepository().get_sport_by_uuid(event_raw.get("sport_uuid"))
            event_raw["sport_id"] = sport.id

            event = Event(**event_raw)
            repository.create_event(event)

            return repository.get_event_by_uuid(event.uuid)
        except SportNotFoundException as err:
            raise EventForeignKeyException()
        except ValidationError as err:
            raise EventValidationErrorException(str(err))


class UpdateEventUsecase:
    def execute(self, uuid: UUID, event_raw: Dict) -> Event:
        repo = EventRepository()
        repo.get_event_by_uuid(uuid)

        sport = SportRepository().get_sport_by_uuid(event_raw.get("sport_uuid"))
        event_raw["sport_id"] = sport.id

        try:
            event = Event(**event_raw)
            event = repo.update_event(uuid, event)

            return event
        except ValidationError as err:
            raise EventValidationErrorException(str(err))
