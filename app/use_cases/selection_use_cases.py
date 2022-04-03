from typing import Dict, List
from uuid import UUID

from pydantic import ValidationError

from ..domain import Selection
from ..repositories.event_repository import EventRepository
from ..repositories.exceptions import (
    EventForeignKeyException,
    EventNotFoundException,
    SelectionValidationErrorException,
)
from ..repositories.selection_repository import SelectionRepository


class ListSelectionUsecase:
    def execute(self, filters: Dict = None) -> List[Selection]:
        repo = SelectionRepository()
        selections = repo.get_selections(filters)
        return selections


class CreateSelectionUsecase:
    def execute(self, selection_raw: Dict) -> Selection:
        repository = SelectionRepository()
        try:
            event = EventRepository().get_event_by_uuid(selection_raw.get("event_uuid"))
            selection_raw["event_id"] = event.id

            selection = Selection(**selection_raw)
            repository.create_selection(selection)

            return repository.get_selection_by_uuid(selection.uuid)
        except EventNotFoundException as err:
            raise EventForeignKeyException()
        except ValidationError as err:
            raise SelectionValidationErrorException(str(err))


class UpdateSelectionUsecase:
    def execute(self, uuid: UUID, selection_raw: Dict) -> Selection:
        repo = SelectionRepository()
        repo.get_selection_by_uuid(uuid)

        event = EventRepository().get_event_by_uuid(selection_raw.get("event_uuid"))
        selection_raw["event_id"] = event.id

        try:
            selection = Selection(**selection_raw)
            selection = repo.update_selection(uuid, selection)
            return selection
        except ValidationError as err:
            raise SelectionValidationErrorException(str(err))
