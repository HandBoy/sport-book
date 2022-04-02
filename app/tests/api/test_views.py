import uuid
from datetime import datetime

from app.domain import EventStatus, EventType


class TestListSports:
    def test_list_sport(self, client):
        # Give
        # Act
        response = client.get("/api/v1/sports")
        # Then
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_get_sports_by_slug(self, client, create_sport):
        # Give
        filters = f"?slug={create_sport.slug}"
        # Act
        response = client.get(f"/api/v1/sports{filters}")
        # Then
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_get_sports_by_slug_and_active(self, client, create_sport):
        # Give
        filters = f"?slug={create_sport.slug}&active=1"
        # Act
        response = client.get(f"/api/v1/sports{filters}")
        # Them
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_get_sports_by_slug_and_active_false(self, client, create_sport):
        # Give
        filters = f"?slug={create_sport.slug}&active=0"
        # Act
        response = client.get(f"/api/v1/sports{filters}")
        # Them
        assert response.status_code == 200
        assert len(response.json) == 0


class TestPostSports:
    def test_create_sport(self, client):
        # Given
        data = {"slug": "john-doe", "active": True}
        # When
        response = client.post("/api/v1/sports", json=data)
        data = response.json
        # Assert
        assert response.status_code == 201

    def test_create_sport_check_contract(self, client):
        # Given
        expected_contract = ["uuid", "slug", "active", "created_at"]
        data = {"slug": "john-doe", "active": True}
        # When
        response = client.post("/api/v1/sports", json=data)
        data = response.json
        # Then
        assert response.status_code == 201
        assert expected_contract, list(data.keys())

    def test_error_create_sport_without_slug(self, client):
        # Given
        data = {"active": True}
        # When
        response = client.post("/api/v1/sports", json=data)
        data = response.json
        # Then
        assert response.status_code == 422


class TestUpdateSports:
    def test_update_sport(self, client, create_sport):
        # Given
        expected_sport = {"slug": "test_updated", "active": False}
        # When
        response = client.put(
            f"/api/v1/sports/{create_sport.uuid}",
            json=expected_sport,
        )

        data = response.json
        # Assert
        assert response.status_code == 200
        assert data.get("slug") == expected_sport.get("slug")
        assert data.get("active") == expected_sport.get("active")

    def test_update_sport_without_slug(self, client, create_sport):
        # Given
        expected_sport = {"active": False}
        # When

        response = client.put(
            f"/api/v1/sports/{str(create_sport.uuid)}",
            json=expected_sport,
        )
        data = response.json
        # Assert
        assert response.status_code == 422

    def test_update_sport_with_unexistent_slug(
        self,
        client,
    ):
        # Given
        expected_sport = {"slug": "test_updated", "active": False}
        # When
        response = client.put(
            f"/api/v1/sports/{str(uuid.uuid4())}",
            json=expected_sport,
        )
        data = response.json
        # Assert
        assert response.status_code == 404
        assert "message" in data
        assert data["message"] == "Sport not found"


class TestListEvents:
    def test_list_events(self, client):
        # Give
        # Act
        response = client.get("/api/v1/events")
        # Then
        assert response.status_code == 200
        assert len(response.json) == 4

    def test_get_events_by_slug(self, client, create_event):
        # Give
        filters = f"?slug={create_event.slug}"
        # Act
        response = client.get(f"/api/v1/events{filters}")
        # Then
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_get_events_by_slug_and_active(self, client, create_event):
        # Give
        filters = f"?slug={create_event.slug}&active=1"
        # Act
        response = client.get(f"/api/v1/events{filters}")
        # Them
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_get_events_by_slug_and_active_false(self, client, create_event):
        # Give
        filters = f"?slug={create_event.slug}&active=0"
        # Act
        response = client.get(f"/api/v1/events{filters}")
        # Them
        assert response.status_code == 200
        assert len(response.json) == 0


class TestPostEvents:
    def make_raw_event(self, create_sport):
        name = "New Event"
        return {
            "sport_uuid": create_sport.uuid,
            "name": name,
            "active": True,
            "event_type": EventType.preplay.value,
            "status": EventStatus.pending.value,
            "scheduled_at": datetime.utcnow().isoformat(),
            "start_at": datetime.utcnow().isoformat(),
        }

    def test_create_event(self, client, create_sport):
        # Given
        data = self.make_raw_event(create_sport)
        # When
        response = client.post("/api/v1/events", json=data)
        data = response.json
        # Assert
        assert response.status_code == 201

    def test_create_event_check_contract(self, client, create_sport):
        # Given
        data = self.make_raw_event(create_sport)
        expected_contract = data.keys()
        # When
        response = client.post("/api/v1/events", json=data)
        data = response.json
        # Then
        assert response.status_code == 201
        assert expected_contract, list(data.keys())

    def test_error_create_event_without_required_fields(self, client):
        # Given
        data = {"active": True}
        # When
        response = client.post("/api/v1/events", json=data)
        # Then
        assert response.status_code == 422

    def test_error_create_event_with_invalid_datetime(self, client, create_sport):
        # Given
        data = self.make_raw_event(create_sport)
        data["start_at"] = "12/02/2022"
        # When
        response = client.post("/api/v1/events", json=data)
        # Then
        assert response.status_code == 422

    def test_error_create_event_with_invalid_event_type(self, client, create_sport):
        # Given
        data = self.make_raw_event(create_sport)
        data["event_type"] = "other"
        headers = {"content-type": "application/json"}
        # When
        response = client.post("/api/v1/events", json=data, headers=headers)
        # Then
        assert response.status_code == 422
        assert "message" in response.json
        assert "code" in response.json

    def test_error_create_event_with_invalid_event_status(self, client, create_sport):
        # Given
        data = self.make_raw_event(create_sport)
        data["status"] = "other"
        headers = {"content-type": "application/json"}
        # When
        response = client.post("/api/v1/events", json=data, headers=headers)
        # Then
        assert response.status_code == 422
        assert "message" in response.json
        assert "code" in response.json
