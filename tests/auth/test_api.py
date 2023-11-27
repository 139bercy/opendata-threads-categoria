from app import server as app


def test_valid_login():
    # Arrange
    client = app.test_client()
    data = {"username": "jdoe", "password": "password"}
    # Act
    response = client.post("/login", json=data)
    # Assert
    assert response.status_code == 200
    assert "message" in response.json
    assert "token" in response.json


def test_invalid_credentials():
    # Arrange
    client = app.test_client()
    data = {"username": "jdoe", "password": "Oops!"}
    # Act
    response = client.post("/login", json=data)
    # Assert
    assert response.status_code == 401
    assert "error" in response.json
