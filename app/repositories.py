from typing import List

from .domain import Sport
from .ext.database import get_db


class SportRepository:
    def __init__(self) -> List[Sport]:
        pass

    def get_sport(self, ):
        db = get_db()
        sports = []

        result = db.execute("SELECT * FROM sport").fetchall()

        for sport in result:
            sports.append(Sport(**sport))

        return sports
