import uuid
from http import HTTPStatus

from app.api.exceptions import (
    ApiEventNotFound,
    ApiEventValidationError,
    ApiSportNotFound,
)
from app.repositories.exceptions import (
    EventNotFoundException,
    EventValidationErrorException,
)
from app.repositories.sport_repository import SportNotFoundException
from app.use_cases.event_use_cases import (
    CreateEventUsecase,
    ListEventUsecase,
    UpdateEventUsecase,
)
from app.use_cases.sport_use_cases import (
    CreateSportsUsecase,
    ListSportsUsecase,
    UpdateSportsUsecase,
)
from flask import request
from flask_apispec import MethodResource, doc, marshal_with, use_kwargs

from .serializers.schemas import (
    EventInSchema,
    EventOutSchema,
    SportInSchema,
    SportOutSchema,
)


@doc(description="a pet store", tags=["sport"])
class SportsListView(MethodResource):
    @marshal_with(SportOutSchema(many=True))
    def get(self):
        filters = request.args.to_dict()
        use_case = ListSportsUsecase()
        sports = use_case.execute(filters)
        return sports

    @use_kwargs(SportInSchema)
    @marshal_with(SportOutSchema, code=HTTPStatus.CREATED)
    def post(self, **kwargs):
        use_case = CreateSportsUsecase()
        sport_raw = use_case.execute(kwargs)

        return sport_raw.dict(), 201


@doc(description="a pet store", tags=["sport"])
class SportsView(MethodResource):
    @use_kwargs(SportInSchema)
    @marshal_with(SportOutSchema, code=HTTPStatus.OK)
    def put(self, sport_uuid: uuid.UUID, **kwargs):
        use_case = UpdateSportsUsecase()
        try:
            sport_raw = use_case.execute(sport_uuid, kwargs)
        except SportNotFoundException as err:
            raise ApiSportNotFound()

        return sport_raw.dict(), 200


@doc(description="events endpoint", tags=["event"])
class EventListView(MethodResource):
    @marshal_with(EventOutSchema(many=True), code=HTTPStatus.OK)
    def get(self):
        filters = request.args.to_dict()
        use_case = ListEventUsecase()
        events = use_case.execute(filters)

        return events

    @use_kwargs(EventInSchema)
    @marshal_with(EventOutSchema, code=HTTPStatus.CREATED)
    def post(self, **kwargs):
        use_case = CreateEventUsecase()

        try:
            event = use_case.execute(kwargs)
            return event.dict(), 201

        except EventValidationErrorException as err:
            raise ApiEventValidationError(str(err))


@doc(description="a pet store", tags=["event"])
class EventView(MethodResource):
    @use_kwargs(EventInSchema)
    @marshal_with(EventOutSchema, code=HTTPStatus.OK)
    def put(self, event_uuid: uuid.UUID, **kwargs):
        use_case = UpdateEventUsecase()
        try:
            event = use_case.execute(event_uuid, kwargs)
        except SportNotFoundException as err:
            raise ApiSportNotFound()
        except EventNotFoundException as err:
            raise ApiEventNotFound()
        except EventValidationErrorException as err:
            raise ApiEventValidationError(str(err))

        return event.dict(), 200
