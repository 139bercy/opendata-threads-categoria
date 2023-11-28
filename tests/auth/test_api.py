from app import server as app


def test_valid_login():
    # Arrange
    client = app.test_client()
    data = {"username": "jdoe", "password": "password"}
    # Act
    response = client.post("/login", data=data)
    # Assert
    assert response.status_code == 200
    assert "message" in response.json
    assert "token" in response.json


def test_invalid_username():
    # Arrange
    client = app.test_client()
    data = {"username": "Oops!", "password": "password"}
    # Act
    response = client.post("/login", data=data)
    # Assert
    assert response.status_code == 200
    assert "Invalid credentials" in response.text


def test_invalid_password():
    # Arrange
    client = app.test_client()
    data = {"username": "jdoe", "password": "Oops!"}
    # Act
    response = client.post("/login", json=data)
    # Assert
    assert response.status_code == 200
    assert "Invalid credentials" in response.text
