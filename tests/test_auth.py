from fastapi import status

from tests.helpers import create_user, login_user


class TestAuthLogin:
    def test_login_success(self, client):
        create_user(
            client,
            email="auth@example.com",
            password="secret123",
        )

        response = client.post(
            "/auth/login",
            json={
                "email": "auth@example.com",
                "password": "secret123",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_password(self, client):
        create_user(
            client,
            email="auth@example.com",
            password="secret123",
        )

        response = client.post(
            "/auth/login",
            json={
                "email": "auth@example.com",
                "password": "wrongpassword",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_unknown_email(self, client):
        response = client.post(
            "/auth/login",
            json={
                "email": "unknown@example.com",
                "password": "secret123",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthProtection:
    def test_protected_endpoint_requires_token(self, client):
        response = client.post(
            "/exercises",
            json={
                "name": "Push-up",
                "description": "Bodyweight pushing exercise",
                "muscles": [],
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_invalid_token(self, client):
        response = client.post(
            "/exercises",
            json={
                "name": "Push-up",
                "description": "Bodyweight pushing exercise",
                "muscles": [],
            },
            headers={
                "Authorization": "Bearer invalid.token",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_valid_token(self, client):
        create_user(
            client,
            email="auth@example.com",
            password="secret123",
        )

        token = login_user(
            client,
            email="auth@example.com",
            password="secret123",
        )

        response = client.post(
            "/exercises",
            json={
                "name": "Push-up",
                "description": "Bodyweight pushing exercise",
                "muscles": [],
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
