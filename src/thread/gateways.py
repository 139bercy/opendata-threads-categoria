import abc

from src.thread.models import Message, Thread


class AbstractThreadRepository(abc.ABC):
    @abc.abstractmethod
    def get_message_by_sk(self, sk: str) -> Message:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_thread_by_sk(self, sk: str) -> Thread:
        pass  # pragma: no cover

    @abc.abstractmethod
    def create(self, message: Message) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_thread(self, thread: Thread) -> None:
        pass  # pragma: no cover
