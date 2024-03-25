import abc

from src.core.models import Message, Thread, Dataset


class AbstractThreadRepository(abc.ABC):
    @abc.abstractmethod
    def get_message_by_sk(self, sk: str) -> Message:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_thread_by_sk(self, sk: str) -> Thread:
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_message(self, message: Message) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_thread(self, thread: Thread) -> None:
        pass  # pragma: no cover


class AbstractDatasetRepository(abc.ABC):
    @abc.abstractmethod
    def create_dataset(self, dataset: Dataset) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_dataset_by_buid(self, buid: str) -> Dataset:
        pass  # pragma: no cover
