from dataclasses import dataclass
from uuid import UUID


@dataclass
class Account:
    def __init__(
        self,
        pk: int,
        sk: UUID,
        username: str,
        email: str,
        password: str,
        token: str,
    ):
        self.pk = pk
        self.sk = sk
        self.username = username
        self.email = email
        self.password = password
        self.token = token

    @property
    def is_logged_in(self):
        if self.token is not None:
            return True
        return False

    def token_is_valid(self, token):
        return str(self.token) == str(token)
