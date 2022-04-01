import uuid
from http import HTTPStatus

from app.api.exceptions import ApiSportNotFound
from app.repositories.sport_repository import SportNotFoundException
from app.use_cases.sport_use_cases import (
    CreateSportsUsecase,
    ListSportsUsecase,
    UpdateSportsUsecase,
)
from flask import request
from flask_apispec import MethodResource, doc, marshal_with, use_kwargs

from .serializers.sport_schemas import SportInSchema, SportOutSchema


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
        sport_raw = SportInSchema().load(kwargs)

        use_case = CreateSportsUsecase()
        sport_raw = use_case.execute(sport_raw)

        return sport_raw.dict(), 201


@doc(description="a pet store", tags=["sport"])
class SportsView(MethodResource):
    @use_kwargs(SportInSchema)
    @marshal_with(SportOutSchema, code=HTTPStatus.OK)
    def put(self, sport_id: uuid.UUID, **kwargs):
        sport_raw = SportInSchema().load(kwargs)

        use_case = UpdateSportsUsecase()
        try:
            sport_raw = use_case.execute(sport_id, sport_raw)
        except SportNotFoundException as err:
            raise ApiSportNotFound()

        return sport_raw.dict(), 200
