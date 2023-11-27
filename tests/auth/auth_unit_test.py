from src.auth.infrastructure import AccountInMemoryRepository
from src.auth.usecases import retrieve_user


def test_retrieve_user():
    # Arrange
    repository = AccountInMemoryRepository()
    # Act
    result = retrieve_user(repository=repository, username="jdoe")
    # Assert
    assert result.username == "jdoe"
