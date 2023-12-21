from src.core.infrastructure import InMemoryThreadRepository
from src.core.models import Message, Thread
from src.core.usecases import create_message, create_thread


def test_create_message():
    # Arrange
    repository = InMemoryThreadRepository([])
    # Act
    message = create_message(
        repository=repository,
        thread_id="7665a9eacdd3c3173bb2d30c",
        author="jdoe",
        content="Hello, World!",
        posted_on="2023-01-01 12:00:00",
    )
    # Assert
    assert isinstance(message, Message)
    assert message.sk == "78d750d4"


def test_get_message():
    # Arrange
    expected = {
        "pk": 1,
        "sk": "78d750d4",
        "thread_id": "7665a9eacdd3c3173bb2d30c",
        "posted_on": "2023-01-01 12:00:00",
        "author": "jdoe",
        "content": "Hello, World!",
    }
    repository = InMemoryThreadRepository(db=[expected])
    # Act
    resource = repository.get_message_by_sk("78d750d4")
    assert resource.__dict__ == expected


def test_create_thread():
    # Arrange
    repository = InMemoryThreadRepository([])
    # Act
    thread = create_thread(
        repository=repository,
        title="Lorem ipsum",
    )
    # Assert
    assert isinstance(thread, Thread)
    assert thread.sk == "a9a66978"


def test_get_thread():
    # Arrange
    expected = {
        "pk": 1,
        "sk": "78d750d4",
        "title": "Lorem ipsum",
    }
    repository = InMemoryThreadRepository(db=[expected])
    # Act
    resource = repository.get_thread_by_sk("78d750d4")
    assert resource.__dict__ == expected
