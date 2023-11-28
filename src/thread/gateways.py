import abc

from src.thread.models import Message


class AbstractThreadRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_bk(self, sk: str) -> Message:
        pass

    @abc.abstractmethod
    def create(self, message: Message) -> None:
        pass
