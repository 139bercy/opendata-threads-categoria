from src.infrastructure.client import postgres_client
from src.thread.infrastructure import PostgresThreadRepository
from tests.thread.test_models import create_message


def test_create_message(db_fixture):
    # Act
    repository = PostgresThreadRepository()
    # Arrange
    message = create_message(
        repository=repository, author="jdoe", content="Hello, World!", created_at="2023-01-01 12:00:00"
    )
    # Assert
    result = postgres_client.fetch_one("SELECT * FROM message;")
    assert result["bk"] == message.bk
