import pytest

from src.auth.infrastructure import AccountInMemoryRepository
from src.auth.models import hash_password
from src.auth.usecases import retrieve_user, login, UserDoesNotExistsError


def test_retrieve_user():
    # Arrange
    repository = AccountInMemoryRepository()
    # Act
    result = retrieve_user(repository=repository, username="jdoe")
    # Assert
    assert result["username"] == "jdoe"


def test_hash_password():
    # Arrange
    password = "password"
    hashed = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    # Act
    result = hash_password(password)
    # Assert
    assert result == hashed


def test_valid_credentials():
    # Arrange
    repository = AccountInMemoryRepository()
    username = "jdoe"
    password = "password"
    # Act
    result = login(repository=repository, username=username, password=password)
    # Assert
    assert result is True


def test_invalid_username():
    # Arrange
    repository = AccountInMemoryRepository()
    username = "Oops!"
    password = "password"
    # Act & Assert
    with pytest.raises(UserDoesNotExistsError):
        login(repository=repository, username=username, password=password)


def test_invalid_password():
    pass


def test_empty_credentials():
    pass


def test_missing_username():
    pass


def test_missing_password():
    pass


def test_long_username():
    pass


def test_long_password():
    pass
