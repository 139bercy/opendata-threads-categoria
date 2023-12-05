from uuid import UUID

import pytest

from src.auth.exceptions import LoginError, UsernameError
from src.auth.infrastructure import InMemoryAccountRepository
from src.auth.usecases import is_logged_in, retrieve_account, login, encode_token, check_token, InvalidToken
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


def test_format_token():
    # Arrange
    username = "jdoe"
    token = UUID("1aab03db-d323-4c55-aa52-33913ed821d7")
    # Act
    result = encode_token(username=username, token=token)
    # Assert
    assert result == "amRvZToxYWFiMDNkYi1kMzIzLTRjNTUtYWE1Mi0zMzkxM2VkODIxZDc="


def test_check_token_is_invalid():
    # Arrange
    repository = InMemoryAccountRepository()
    token = "amRvZToxYWFiMDNkYi1kMzIzLTRjNTUtYWE1Mi0zMzkxM2VkODIxZDc="
    # Act @ Assert
    with pytest.raises(InvalidToken):
        check_token(repository=repository, encoded_token=token)


def test_check_token_is_valid():
    # Arrange
    repository = InMemoryAccountRepository()
    token = "anNtaXRoOmQ2YTgxM2RlLTczYzEtNDMyOC1hYTU1LTBhYzFhMDEyMGIyMA=="
    # Act
    result = check_token(repository=repository, encoded_token=token)
    # Assert
    assert result


def test_valid_credentials():
    # Arrange
    repository = InMemoryAccountRepository()
    # Act
    result = login(repository=repository, username="jdoe", password="password")
    # Assert
    assert type(result) is str
    assert len(result) == 56


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
