from sqlite3 import OperationalError
from typing import Dict, List
from uuid import UUID

from ..domain import Event
from ..ext.database import get_db
from . import generate_query_filter
from .exceptions import EventNotFoundException, RepositoryOperationalError


class EventRepository:
    def __init__(self) -> None:
        self.db = get_db()

    def get_events(self, filters: Dict = None) -> List[Event]:
        events = []
        parameters = ()

        query = "SELECT * FROM event "

        if filters:
            query += generate_query_filter(filters)
            parameters = tuple(filters.values())

        try:
            result = self.db.execute(query, parameters).fetchall()
        except OperationalError as err:
            raise RepositoryOperationalError(str(err))

        for event in result:
            events.append(Event(**event))

        return events

    def get_event_by_uuid(self, uuid: UUID) -> Event:
        result = self.db.execute(
            "SELECT * FROM event WHERE uuid = ?",
            (str(uuid),),
        ).fetchone()

        if result is None:
            raise EventNotFoundException()

        return Event(**result)

    def create_event(self, event: Event):
        self.db.execute(
            (
                "INSERT INTO event (sport_id, uuid, name, slug, active, event_type, status, scheduled_at, start_at)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            ),
            (
                event.sport_id,
                str(event.uuid),
                event.name,
                event.slug,
                event.active,
                event.event_type.value,
                event.status.value,
                event.scheduled_at,
                event.start_at,
            ),
        )
        self.db.commit()
