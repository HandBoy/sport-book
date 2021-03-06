from typing import Dict, List
from uuid import UUID

from pydantic import ValidationError

from ..domain import Sport
from ..repositories.exceptions import SportValidationErrorException
from ..repositories.sport_repository import SportRepository


class ListSportsUsecase:
    def execute(self, filters: Dict = None) -> List[Sport]:
        repo = SportRepository()
        sports = repo.get_sport(filters)
        return sports


class GetSportByUUIDUsecase:
    def execute(self, uuid: UUID) -> Sport:
        repo = SportRepository()
        sport = repo.get_sport_by_uuid(uuid)
        return sport


class GetSportByIdUsecase:
    def execute(self, id: int) -> Sport:
        repo = SportRepository()
        sport = repo.get_sport_by_id(id)
        return sport


class CreateSportsUsecase:
    def execute(self, sport_raw: Dict) -> Sport:
        repo = SportRepository()
        try:
            sport = Sport(**sport_raw)
            sport = repo.create_sport(sport)
            return sport
        except ValidationError as ex:
            raise SportValidationErrorException(ex.errors)


class UpdateSportsUsecase:
    def execute(self, uuid: UUID, sport_raw: Dict) -> Sport:
        repo = SportRepository()
        repo.get_sport_by_uuid(uuid)

        try:
            sport = Sport(**sport_raw)
        except ValidationError as ex:
            raise SportValidationErrorException(ex.errors)

        sport = repo.update_sport(uuid, sport)
        return sport


class InactivateSportUseCase:
    def execute(self, sport_uuid: UUID) -> Sport:
        sport = GetSportByUUIDUsecase().execute(sport_uuid)
        sport.active = False

        return UpdateSportsUsecase().execute(sport.uuid, sport.dict())
