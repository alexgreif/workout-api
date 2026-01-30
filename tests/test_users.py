from fastapi import status
from tests.helpers import create_user


class TestCreateUser:
    def test_create_user(self, client):
        response = client.post(
            "/users",
            json={
                "email": "test@example.com",
                "password": "secret123",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["email"] == "test@example.com"
        assert "id" in data

        # Security guarantees
        assert "password" not in data
        assert "password_hash" not in data

    def test_create_user_invalid_email(self, client):
        response = client.post(
            "/users",
            json={
                "email": "testexample.com",
                "password": "secret123",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_invalid_password_type(self, client):
        response = client.post(
            "/users",
            json={
                "email": "test@example.com",
                "password": 123,
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_missing_email(self, client):
        response = client.post(
            "/users",
            json={
                "password": "secret123",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_missing_password(self, client):
        response = client.post(
            "/users",
            json={
                "email": "test@example.com",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_duplicate_email(self, client):
        client.post(
            "/users",
            json={
                "email": "duplicate@example.com",
                "password": "secret123",
            },
        )

        response = client.post(
            "/users",
            json={
                "email": "duplicate@example.com",
                "password": "secret123",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT


class TestGetUser:
    def test_get_user(self, client):
        user_id = create_user(
            client,
            email="getme@example.com",
            password="secret123"
        )

        response = client.get(f"/users/{user_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["email"] == "getme@example.com"
        assert "password" not in data
        assert "password_hash" not in data

    def test_get_user_not_found(self, client):
        response = client.get("/users/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_user_invalid_id(self, client):
        response = client.get("/users/abc")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
