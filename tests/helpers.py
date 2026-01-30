from fastapi import status


class UserNotCreatedError(Exception):
    def __init__(self, email, status_code):
        super().__init__(
            f"Failed to create user {email} (status={status_code})"
        )


class ExerciseNotCreatedError(Exception):
    def __init__(self, name, status_code):
        super().__init__(
            f"Failed to create exercise {name} (status={status_code})"
        )


def create_user(client, *, email="user@example.com", password="secret123"):
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


def create_exercise(client, *, name, description, muscles, user):
    response = client.post(
            "/exercises",
            json={
                "name": name,
                "description": description,
                "muscles": muscles,
            },
            headers={
                "X-User-Id": str(user),
            },
        )

    if response.status_code != status.HTTP_201_CREATED:
        raise ExerciseNotCreatedError(name, response.status_code)

    return response.json()["id"]
