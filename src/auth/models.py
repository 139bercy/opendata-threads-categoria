import hashlib
from uuid import UUID
from dataclasses import dataclass


@dataclass
class Account:
    def __init__(
        self,
        pk: int,
        uuid: UUID,
        username: str,
        email: str,
        password: str,
        token: str,
    ):
        self.pk = pk
        self.uuid = uuid
        self.username = username
        self.email = email
        self.password = password
        self.token = token

    @property
    def is_logged_in(self):
        if self.token is not None:
            return True
        return False


def hash_password(chain):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(chain.encode("utf-8"))
    return sha256_hash.hexdigest()
