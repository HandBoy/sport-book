from typing import List
from uuid import UUID

from .domain import Sport
from .ext.database import get_db


class SportRepositoryException(Exception):
    pass


class SportValidationErrorException(SportRepositoryException):
    pass


class SportNotFoundException(SportRepositoryException):
    def __init__(self):
        Exception.__init__(self)
        self.message = "Sport not found"


class SportIntegrityError(SportRepositoryException):
    def __init__(self, message):
        self.message = message

class SportRepository:
    def __init__(self) -> None:
        self.db = get_db()

    def get_sport(self) -> List[Sport]:
        sports = []

        result = self.db.execute("SELECT * FROM sport").fetchall()

        for sport in result:
            sports.append(Sport(**sport))

        return sports

    def get_sport_by_id(self, id: int):
        result = self.db.execute(
            "SELECT * FROM sport WHERE id = ?",
            (id,),
        ).fetchone()

        if result is None:
            raise SportNotFoundException()

        return Sport(**result)

    def get_sport_by_uuid(self, uuid: UUID):
        result = self.db.execute(
            "SELECT * FROM sport WHERE uuid = ?",
            (str(uuid),),
        ).fetchone()

        if result is None:
            raise SportNotFoundException()

        return Sport(**result)

    def create_sport(self, sport: Sport) -> Sport:
        result = self.db.execute(
            "INSERT INTO sport (uuid, slug, active) VALUES (?, ?, ?)",
            (str(sport.uuid), sport.slug, sport.active),
        )
        self.db.commit()

        return self.get_sport_by_id(result.lastrowid)

    def update_sport(self, uuid: UUID, sport: Sport) -> Sport:
        self.db.execute(
            "UPDATE sport SET slug = ?, active = ? WHERE uuid = ?",
            (sport.slug, sport.active, str(uuid)),
        ).fetchone()

        self.db.commit()

        return self.get_sport_by_uuid(uuid)
