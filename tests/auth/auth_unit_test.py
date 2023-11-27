from src.auth.infrastructure import AccountInMemoryRepository
from src.auth.usecases import retrieve_user


def test_retrieve_user():
    # Arrange
    repository = AccountInMemoryRepository()
    # Act
    result = retrieve_user(repository=repository, username="jdoe")
    # Assert
    assert result.username == "jdoe"


def test_valid_credentials():
    pass


def test_invalid_username():
    pass


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
