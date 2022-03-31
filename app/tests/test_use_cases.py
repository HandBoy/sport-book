import uuid

import pytest
from app.repositories import SportNotFoundException, SportValidationErrorException
from app.use_cases import CreateSportsUsecase, ListSportsUsecase, UpdateSportsUsecase


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


class TestUpdateSportsUsecase:
    def test_update_sport(self, app, create_sport):
        # Give
        use_case = UpdateSportsUsecase()
        data = {
            "slug": "test-01-updated",
            "active": True,
        }
        # Act
        sport = use_case.execute(create_sport.uuid, data)
        # Them
        assert sport != None
        assert sport.slug == data.get("slug")
        assert sport.active == data.get("active")

    def test_update_sport_with_unexistent_sport(self, app):
        # Give
        use_case = UpdateSportsUsecase()
        data = {
            "slug": "test-01-updated",
            "active": True,
        }
        uid = uuid.uuid4()
        # Them
        with pytest.raises(SportNotFoundException):
            # Act
            use_case.execute(uid, data)

    def test_update_sport_without_slug(self, app, create_sport):
        # Give
        use_case = UpdateSportsUsecase()
        data = {"active": True}
        # Them
        with pytest.raises(SportValidationErrorException):
            # Act
            use_case.execute(create_sport.uuid, data)
