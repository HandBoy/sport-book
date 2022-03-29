from typing import Dict, List

from app.domain import Sport
from app.repositories import SportRepository


class ListSportsUsecase:
    def execute(self) -> List[Sport]:
        repo = SportRepository()
        sports = repo.get_sport()
        return sports


class CreateSportsUsecase:
    def execute(self, sport: Sport) -> Sport:
        repo = SportRepository()
        sports = repo.create_sport(sport)
        return sports
