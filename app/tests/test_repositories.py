import uuid

import pytest
from app.domain import Sport
from app.repositories import SportNotFoundException, SportRepository


class TestSportRepository:
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
