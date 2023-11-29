import hashlib
from uuid import UUID
from dataclasses import dataclass


@dataclass
class Account:
    source = "coucou"

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
