from src.common import sha256_hash_string


class Message:
    def __init__(self, bk: str, author: str, content: str, created_at: str, pk: int = None):
        self.pk = pk
        self.created_at = created_at
        self.author = author
        self.content = content
        self.bk = bk

    @classmethod
    def create(cls, author: str, content: str, created_at: str):
        bk = get_key(content)
        instance = cls(bk=bk, author=author, content=content, created_at=created_at)
        return instance


def get_key(chain):
    return sha256_hash_string(chain)[0:8]
