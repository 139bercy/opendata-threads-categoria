from src.thread.infrastructure import InMemoryThreadRepository
from src.thread.models import Message


def create_message(repository, author, content, created_at):
    message = Message.create(author=author, content=content, created_at=created_at)
    repository.create(message)
    return message


def test_create_message():
    # Act
    repository = InMemoryThreadRepository([])
    expected = {
        "pk": 1,
        "bk": "dffd6021",
        "created_at": "2023-01-01 12:00:00",
        "author": "jdoe",
        "content": "Hello, World!",
    }
    # Arrange
    message = create_message(
        repository=repository, author="jdoe", content="Hello, World!", created_at="2023-01-01 12:00:00"
    )
    # Assert
    resource = repository.get_by_bk("dffd6021")
    assert isinstance(message, Message)
    assert message.__dict__ == expected
    assert resource.__dict__ == message.__dict__
