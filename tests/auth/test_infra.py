from uuid import UUID

import pytest

from src.auth.exceptions import LoginError
from src.auth.infrastructure import AccountPostgresqlRepository
from src.auth.usecases import retrieve_account, login


def test_retrieve_postgres_user():
    # Arrange
    repository = AccountPostgresqlRepository()
    # Act
    result = retrieve_account(repository=repository, username="jdoe")
    # Assert
    assert result.username == "jdoe"


def test_postgres_login_with_valid_credentials():
    # Arrange
    repository = AccountPostgresqlRepository()
    repository.update_token("jdoe", None)
    # Act
    result = login(repository=repository, username="jdoe", password="password")
    # Assert
    resource = repository.get_by_username("jdoe")
    assert type(result) == UUID
    assert resource.token is not None


def test_postgres_login_with_invalid_credentials():
    # Arrange
    repository = AccountPostgresqlRepository()
    # Act & Assert
    with pytest.raises(LoginError):
        login(repository=repository, username="jdoe", password="Oops!")
