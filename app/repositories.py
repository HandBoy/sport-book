from typing import List

from .domain import Sport
from .ext.database import get_db


class SportRepository:
    def __init__(self) -> None:
        self.db = get_db()

    def get_sport(self) -> List:
        sports = []

        result = self.db.execute("SELECT * FROM sport").fetchall()

        for sport in result:
            sports.append(Sport(**sport))

        return sports

    def get_sport_by_id(self, id: int):
        result = self.db.execute(
            "SELECT * FROM sport WHERE id = ?", (id,)
        ).fetchone()

        return Sport(**result)

    def create_sport(self, sport_raw: Sport):
        sport = Sport(**sport_raw)
        result = self.db.execute(
            "INSERT INTO sport (uuid, slug, active)" " VALUES (?, ?, ?)",
            (str(sport.uuid), sport.slug, sport.active),
        )
        self.db.commit()

        return self.get_sport_by_id(result.lastrowid)
