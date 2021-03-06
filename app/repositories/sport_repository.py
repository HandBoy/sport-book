from typing import Dict, List
from uuid import UUID

from . import generate_query_filter

from .exceptions import SportNotFoundException

from ..domain import Sport
from ..ext.database import get_db


class SportRepository:
    def __init__(self) -> None:
        self._db = get_db()

    def get_sport(self, filters: Dict = None) -> List[Sport]:
        sports = []
        parameters = ()

        query = "SELECT * FROM sport "

        if filters:
            query += generate_query_filter(filters)
            parameters = tuple(filters.values())

        result = self._db.execute(query, parameters).fetchall()

        for sport in result:
            sports.append(Sport(**sport))

        return sports

    def get_sport_by_id(self, id: int) -> Sport:
        result = self._db.execute(
            "SELECT * FROM sport WHERE id = ?",
            (id,),
        ).fetchone()

        if result is None:
            raise SportNotFoundException()

        return Sport(**result)

    def get_sport_by_uuid(self, uuid: UUID) -> Sport:
        result = self._db.execute(
            "SELECT * FROM sport WHERE uuid = ?",
            (str(uuid),),
        ).fetchone()

        if result is None:
            raise SportNotFoundException()

        return Sport(**result)

    def create_sport(self, sport: Sport) -> Sport:
        result = self._db.execute(
            "INSERT INTO sport (uuid, slug, active) VALUES (?, ?, ?)",
            (str(sport.uuid), sport.slug, sport.active),
        )
        self._db.commit()

        return self.get_sport_by_id(result.lastrowid)

    def update_sport(self, uuid: UUID, sport: Sport) -> Sport:
        self._db.execute(
            "UPDATE sport SET slug = ?, active = ? WHERE uuid = ?",
            (sport.slug, sport.active, str(uuid)),
        )

        self._db.commit()

        return self.get_sport_by_uuid(uuid)
