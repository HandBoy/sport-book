from http import HTTPStatus

from app.use_cases import CreateSportsUsecase, ListSportsUsecase
from flask import jsonify
from flask_apispec import MethodResource, doc, marshal_with, use_kwargs

from .serializers.in_bound import SportRequestSchema
from .serializers.out_bound import SportResponseSchema


@doc(description="a pet store", tags=["sport"])
class SportsView(MethodResource):
    @marshal_with(SportResponseSchema(many=True))
    def get(self):
        use_case = ListSportsUsecase()
        sports = use_case.execute()
        return sports

    @use_kwargs(SportRequestSchema)
    @marshal_with(SportResponseSchema, code=HTTPStatus.CREATED)
    def post(self, **kwargs):
        sport_raw = SportRequestSchema().load(kwargs)

        use_case = CreateSportsUsecase()
        sport_raw = use_case.execute(sport_raw)

        return sport_raw.dict(), 201
