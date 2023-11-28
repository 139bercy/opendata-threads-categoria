import abc


class AbstractAccountRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_username(self, username: str):
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_token(self, username, token):
        pass  # pragma: no cover
