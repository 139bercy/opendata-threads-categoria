from src.auth.usecases import retrieve_user
from src.auth.infrastructure import AccountPostgresqlRepository


def test_retrieve_postgres_user():
    # Arrange
    repository = AccountPostgresqlRepository()
    # Act
    result = retrieve_user(repository=repository, username="jdoe")
    # Assert
    assert result["username"] == "jdoe"
