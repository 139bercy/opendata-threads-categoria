from src.thread.infrastructure import InMemoryThreadRepository
from src.thread.models import Message
from src.thread.usecases import create_message


def test_create_message():
    # Act
    repository = InMemoryThreadRepository([])
    # Arrange
    message = create_message(
        repository=repository,
        thread_id="7665a9eacdd3c3173bb2d30c",
        author="jdoe",
        content="Hello, World!",
        posted_on="2023-01-01 12:00:00",
    )
    # Assert
    assert isinstance(message, Message)
    assert message.bk == "78d750d4"


def test_get_message():
    # Arrange
    expected = {
        "pk": 1,
        "bk": "78d750d4",
        "thread_id": "7665a9eacdd3c3173bb2d30c",
        "posted_on": "2023-01-01 12:00:00",
        "author": "jdoe",
        "content": "Hello, World!",
    }
    repository = InMemoryThreadRepository([expected])
    # Act
    resource = repository.get_by_bk("78d750d4")
    assert resource.__dict__ == expected
