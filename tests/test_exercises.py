from fastapi import status
from tests.helpers import create_user, create_exercise


class TestCreateExercise:
    def test_create_exercise_without_muscles(self, client):
        user_id = create_user(client)

        response = client.post(
            "/exercises",
            json={
                "name": "Push-up",
                "description": "Bodyweight pushing exercise",
                "muscles": [],
            },
            headers={
                "X-User-Id": str(user_id),
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["name"] == "Push-up"
        assert data["description"] == "Bodyweight pushing exercise"
        assert "id" in data

    def test_create_exercise_with_muscles(self, client):
        user_id = create_user(client)

        response = client.post(
            "/exercises",
            json={
                "name": "Bench Press",
                "description": "Classic chest exercise",
                "muscles": [
                    {"muscle_id": 1, "role": "primary"},
                    {"muscle_id": 2, "role": "secondary"},
                ],
            },
            headers={
                "X-User-Id": str(user_id),
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["name"] == "Bench Press"
        assert "id" in data

    def test_create_exercise_missing_name(self, client):
        user_id = create_user(client)

        response = client.post(
            "/exercises",
            json={
                "description": "No name provided",
                "muscles": [],
            },
            headers={
                "X-User-Id": str(user_id),
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_exercise_invalid_muscle_id(self, client):
        user_id = create_user(client)

        response = client.post(
            "/exercises",
            json={
                "name": "Invalid Muscle Exercise",
                "description": None,
                "muscles": [
                    {"muscle_id": 99999, "role": "primary"},
                ],
            },
            headers={
                "X-User-Id": str(user_id),
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_exercise_invalid_muscle_role(self, client):
        user_id = create_user(client)

        response = client.post(
            "/exercises",
            json={
                "name": "Weird Role Exercise",
                "description": None,
                "muscles": [
                    {"muscle_id": 1, "role": "tertiary"},
                ],
            },
            headers={
                "X-User-Id": str(user_id),
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestGetExercises:
    def test_list_exercises(self, client):
        user_id = create_user(client)

        exercise_id = create_exercise(
            client,
            name="Squat",
            description=None,
            muscles= [{"muscle_id": 4, "role": "primary"}],
            user=user_id
        )

        response = client.get("/exercises/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert len(data) >= 1
        assert "name" in data[0]
        assert "id" in data[0]


class TestGetExercise:
    def test_get_exercise_by_id(self, client):
        user_id = create_user(client)
        
        exercise_id = create_exercise(
            client,
            name="Deadlift",
            description="Hip hinge movement",
            muscles= [],
            user=user_id
        )

        response = client.get(f"/exercises/{exercise_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["name"] == "Deadlift"
        assert data["id"] == exercise_id

    def test_get_exercise_not_found(self, client):
        response = client.get("/exercises/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_exercise_invalid_id(self, client):
        response = client.get("/exercises/abc")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
