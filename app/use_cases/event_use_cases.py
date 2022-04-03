from typing import Dict, List
from uuid import UUID

from app.repositories.sport_repository import SportRepository
from pydantic import ValidationError

from app.use_cases.sport_use_cases import (
    GetSportByIdUsecase,
    GetSportByUUIDUsecase,
    InactivateSportUseCase,
)

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


class GetEventByUUIDUsecase:
    def execute(self, uuid: UUID) -> Event:
        repo = EventRepository()
        event = repo.get_event_by_uuid(uuid)
        return event


class GetEventByIUsecase:
    def execute(self, id: int) -> Event:
        repo = EventRepository()
        event = repo.get_event_by_id(id)
        return event


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

        sport = GetSportByUUIDUsecase().execute(event_raw.get("sport_uuid"))
        event_raw["sport_id"] = sport.id

        try:
            event = Event(**event_raw)
            event = repo.update_event(uuid, event)
            self.inactivate_sport(event_raw, sport.uuid)

            return event
        except ValidationError as err:
            raise EventValidationErrorException(str(err))

    def inactivate_sport(self, event_raw: Dict, sport_uuid: UUID):
        """When all the events of a sport are inactive, the sport becomes inactive"""
        if event_raw["active"]:
            return

        filters = {"sport_id": event_raw["sport_id"]}
        events = ListEventUsecase().execute(filters)
        inactivate_sport = all([not event.active for event in events])

        if inactivate_sport:
            InactivateSportUseCase().execute(sport_uuid)


class InactivateEventUseCase:
    def execute(self, event_uuid: UUID) -> Event:
        event = GetEventByUUIDUsecase().execute(event_uuid)
        event.active = False

        sport = GetSportByIdUsecase().execute(event.sport_id)
        event_raw = event.dict()
        event_raw["active"] = False
        event_raw["sport_uuid"] = sport.uuid

        return UpdateEventUsecase().execute(event.uuid, event_raw)
