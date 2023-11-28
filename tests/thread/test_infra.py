from src.config import postgres_client
from src.thread.infrastructure import PostgresThreadRepository
from tests.thread.test_models import create_message


def test_postgres_create_message(db_fixture):
    # Act
    repository = PostgresThreadRepository()
    # Arrange
    message = create_message(
        repository=repository,
        thread_id="7665a9eacdd3c3173bb2d30c",
        author="jdoe",
        content="Hello, World!",
        posted_on="2023-01-01 12:00:00",
    )
    # Assert
    result = postgres_client.fetch_one("SELECT * FROM message;")
    assert result["sk"] == message.sk


def test_postgres_message_escape_specials_chars(db_fixture):
    # Act
    repository = PostgresThreadRepository()
    # Arrange
    message = create_message(
        repository=repository,
        thread_id="7665a9eacdd3c3173bb2d30c",
        author="jdoe",
        content="J'essaie un truc bizarre",
        posted_on="2023-01-01 12:00:00",
    )
    # Assert
    result = postgres_client.fetch_one("SELECT * FROM message;")
    assert result["sk"] == message.sk
