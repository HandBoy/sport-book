class TestListSports:
    def test_list_sport(self, client):
        # Give

        # Act
        response = client.get(
            "/api/v1/sports",
        )
        # Assert
        assert response.status_code == 200
