from uuid import UUID

import pytest

from src.auth.exceptions import LoginError, UsernameError
from src.auth.infrastructure import InMemoryAccountRepository
from src.auth.usecases import is_logged_in, retrieve_account, login
from src.common.utils import sha256_hash_string


def test_retrieve_user():
    # Arrange
    repository = InMemoryAccountRepository()
    # Act
    result = retrieve_account(repository=repository, username="jdoe")
    # Assert
    assert result.username == "jdoe"


def test_hash_password():
    # Arrange
    password = "password"
    hashed = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    # Act
    result = sha256_hash_string(password)
    # Assert
    assert result == hashed


def test_valid_credentials():
    # Arrange
    repository = InMemoryAccountRepository()
    # Act
    result = login(repository=repository, username="jdoe", password="password")
    # Assert
    resource = repository.get_by_username("jdoe")
    assert type(result) is UUID
    assert resource.token == result


def test_invalid_username():
    # Arrange
    repository = InMemoryAccountRepository()
    username = "Oops!"
    password = "password"
    # Act & Assert
    with pytest.raises(UsernameError):
        login(repository=repository, username=username, password=password)


def test_invalid_password():
    # Arrange
    repository = InMemoryAccountRepository()
    username = "jdoe"
    password = "Oops!"
    # Act & Assert
    with pytest.raises(LoginError):
        login(repository=repository, username=username, password=password)


def test_empty_credentials():
    # Arrange
    repository = InMemoryAccountRepository()
    username = ""
    password = ""
    # Act & Assert
    with pytest.raises(UsernameError):
        login(repository=repository, username=username, password=password)


def test_credentials_not_set():
    # Arrange
    repository = InMemoryAccountRepository()
    username = None
    password = None
    # Act & Assert
    with pytest.raises(UsernameError):
        login(repository=repository, username=username, password=password)


def test_is_logged_in_ok():
    repository = InMemoryAccountRepository()
    result = is_logged_in(repository=repository, username="jsmith")
    assert result is True


def test_is_logged_in_ko():
    repository = InMemoryAccountRepository()
    result = is_logged_in(repository=repository, username="jdoe")
    assert result is False
