from app.domain import Outcome
from app.repositories.event_repository import EventRepository
from app.use_cases.selection_use_cases import UpdateSelectionUsecase


class TestInactivateSelectionUseCase:
    def test_inactivate_all_events(self, app, create_selection):
        # Give
        event = EventRepository().get_event_by_id(create_selection.event_id)
        data = {
            "event_uuid": event.uuid,
            "price": 10.5,
            "active": False,
            "outcome": Outcome.unsettled.value,
        }
        # Act
        UpdateSelectionUsecase().execute(create_selection.uuid, data)
        # Them
        event = EventRepository().get_event_by_id(create_selection.event_id)
        assert event.active == False
