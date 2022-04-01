import uuid

import pytest
from app.domain import Sport
from app.repositories import generate_query_filter
from app.repositories.exceptions import SportNotFoundException
from app.repositories.sport_repository import SportRepository


class TestGetSportRepository:
    def test_get_sports(self, app):
        # Give
        repository = SportRepository()
        # Act
        sports = repository.get_sport()
        # Them
        assert sports != None
        assert len(sports) == 2

    def test_get_sports_by_slug(self, app, create_sport):
        # Give
        filters = {"slug": create_sport.slug}
        repository = SportRepository()
        # Act
        sports = repository.get_sport(filters)
        # Them
        assert sports != None
        assert len(sports) == 1

    def test_get_sports_by_slug_and_active(self, app, create_sport):
        # Give
        filters = {"slug": create_sport.slug, "active": create_sport.active}
        repository = SportRepository()
        # Act
        sports = repository.get_sport(filters)
        # Them
        assert sports != None
        assert len(sports) == 1

    def test_get_sports_by_slug_and_active_false(self, app, create_sport):
        # Give
        filters = {"slug": create_sport.slug, "active": False}
        repository = SportRepository()
        # Act
        sports = repository.get_sport(filters)
        # Them
        assert sports != None
        assert len(sports) == 0

    def test_get_sports_actived(self, app, create_sport):
        # Give
        filters = {"active": True}
        repository = SportRepository()
        # Act
        sports = repository.get_sport(filters)
        # Them
        assert sports != None
        assert len(sports) == 3

class TestCreateSportRepository:
    def test_create_sport(self, app):
        # Give
        repository = SportRepository()
        expected_sport = Sport(slug="test-01", active=True)
        # Act
        sport = repository.create_sport(expected_sport)
        # Them
        assert sport != None
        assert sport.slug == expected_sport.slug
        assert sport.active == expected_sport.active

class TestUpdateSportRepository:
    def test_update_sport(self, app, create_sport):
        # Give
        repository = SportRepository()
        expected_sport = Sport(slug="test-01-updated", active=True)
        # Act
        sport = repository.update_sport(create_sport.uuid, expected_sport)
        # Them
        assert sport != None
        assert sport.slug == expected_sport.slug
        assert sport.active == expected_sport.active

    def test_update_unexistent_sport(self, app):
        # Give
        repository = SportRepository()
        sport = Sport(slug="test-01-updated", active=True)

        uid = uuid.uuid4()
        # Act
        # Them
        with pytest.raises(SportNotFoundException):
            repository.update_sport(uid, sport)


class TestGenerateQueryFilterRepository:
    def test_query_without_filter(self, app):
        # Give
        filters = {}
        query = ""
        # Act
        query = generate_query_filter(filters)
        # Them
        assert query == None

    def test_query_with_one_filter(self, app):
        # Give
        filters = {"one": 1}
        query = ""
        # Act
        query = generate_query_filter(filters)
        # Them
        assert query != ""
        assert "AND" not in query

    def test_query_with_two_filter(self, app):
        # Give
        filters = {"one": 1, "two": 2}
        query = ""
        # Act
        query = generate_query_filter(filters)
        # Them
        assert query == "WHERE one = ? AND two = ? "

    def test_query_with_more_than_two_filter(self, app):
        # Give
        filters = {"one": 1, "two": 2, "more_one": 3}
        query = ""
        # Act
        query = generate_query_filter(filters)
        # Them
        assert query.count("AND") == 2
        assert query == "WHERE one = ? AND two = ? AND more_one = ? "
