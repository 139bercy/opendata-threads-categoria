import hashlib


class Account:
    def __init__(self, username: str):
        self.username = username

    @classmethod
    def create(cls, username: str):
        instance = Account(username)
        return instance


def hash_password(chain):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(chain.encode("utf-8"))
    return sha256_hash.hexdigest()
