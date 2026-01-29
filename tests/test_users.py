def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_user(client):
    create = client.post(
        "/users",
        json={
            "email": "getme@example.com",
            "password": "secret123"
        }
    )
    user_id = create.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "getme@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/99999")
    assert response.status_code == 404
    