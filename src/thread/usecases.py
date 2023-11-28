from src.thread.models import Message


def create_message(repository, thread_id, author, content, posted_on):
    message = Message.create(thread_id=thread_id, author=author, content=content, posted_on=posted_on)
    repository.create(message)
    return message
