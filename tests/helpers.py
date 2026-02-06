from fastapi import status


EXAMPLE_EMAIL = "user@example.com"
EXAMPLE_PASSWORD = "secret123"


class UserNotCreatedError(Exception):
    def __init__(self, email, status_code):
        super().__init__(
            f"Failed to create user {email} (status={status_code})"
        )


class AuthError(Exception):
    def __init__(self, email, status_code):
        super().__init__(
            f"Login failed for {email} (status={status_code})"
        )


class ExerciseNotCreatedError(Exception):
    def __init__(self, name, status_code):
        super().__init__(
            f"Failed to create exercise {name} (status={status_code})"
        )


def create_user(client, *, email=EXAMPLE_EMAIL, password=EXAMPLE_PASSWORD):
    response = client.post(
        "/users",
        json={
            "email": email,
            "password": password,
        },
    )

    if response.status_code != status.HTTP_201_CREATED:
        raise UserNotCreatedError(email, response.status_code)

    return response.json()["id"]


def login_user(client, *, email=EXAMPLE_EMAIL, password=EXAMPLE_PASSWORD):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    if response.status_code != status.HTTP_200_OK:
        raise AuthError(email, response.status_code)
    
    return response.json()["access_token"]


def get_auth_header(
        client, *,
        email=EXAMPLE_EMAIL, password=EXAMPLE_PASSWORD,
        invalid=False
    ):
    try:
        create_user(client, email=email, password=password)
    except UserNotCreatedError:
        pass
    token = login_user(client, email=email, password=password)
    if invalid:
        token = "invalid.token"
    
    return {"Authorization": f"Bearer {token}"}


def create_exercise(
        client, *, name, description, muscles,
        user_email=EXAMPLE_EMAIL, user_password=EXAMPLE_PASSWORD
    ):
    auth_header = get_auth_header(client, email=user_email, password=user_password)
    response = client.post(
            "/exercises",
            json={
                "name": name,
                "description": description,
                "muscles": muscles,
            },
            headers=auth_header
        )

    if response.status_code != status.HTTP_201_CREATED:
        raise ExerciseNotCreatedError(name, response.status_code)

    return response.json()["id"]
