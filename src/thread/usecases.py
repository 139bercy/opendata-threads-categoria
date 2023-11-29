from src.thread.models import Message, Thread
from src.thread.gateways import AbstractThreadRepository


def create_message(
    repository: AbstractThreadRepository, thread_id: str, author: str, content: str, posted_on: str
) -> Message:
    message = Message.create(thread_id=thread_id, author=author, content=content, posted_on=posted_on)
    repository.create(message)
    return message


def create_thread(repository: AbstractThreadRepository, title: str):
    thread = Thread.create(title=title)
    repository.create_thread(thread)
    return thread
