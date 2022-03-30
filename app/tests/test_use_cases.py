import pytest
from app.repositories import SportValidationErrorException
from app.use_cases import CreateSportsUsecase, ListSportsUsecase


class TestListSportsUsecase:
    def test_create_sport(self, app, create_sport):
        # Give
        use_case = ListSportsUsecase()
        # Act
        sports = use_case.execute()
        # Them
        assert len(sports) == 3


class TestCreateSportsUsecase:
    def test_create_sport(self, app):
        # Give
        use_case = CreateSportsUsecase()
        data = {
            "slug": "test-01",
            "active": True,
        }
        # Act
        sport = use_case.execute(data)
        # Them
        assert sport != None

    def test_create_sport_without_slug(self, app):
        # Give
        use_case = CreateSportsUsecase()
        data = {"active": True}
        # Act
        # Them
        with pytest.raises(SportValidationErrorException):
            use_case.execute(data)
