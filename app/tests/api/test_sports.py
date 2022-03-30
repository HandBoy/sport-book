class TestListSports:
    def test_list_sport(self, client):
        # Give
        # Act
        response = client.get("/api/v1/sports")
        # Then
        assert response.status_code == 200
        assert len(response.json) == 2


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
