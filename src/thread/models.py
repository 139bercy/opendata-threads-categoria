import hashlib


class Message:
    def __init__(self, author: str, content: str, created_at: str, bk: str = None):
        self.created_at = created_at
        self.author = author
        self.content = content
        self.bk = bk or get_key(self.content)

    @classmethod
    def create(cls, author: str, content: str, created_at: str):
        instance = cls(author=author, content=content, created_at=created_at)
        return instance

    def __repr__(self):
        return f"<Message: {self.bk}>"


def sha256_hash_string(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode("utf-8"))
    return sha256_hash.hexdigest()


def get_key(chain):
    return sha256_hash_string(chain)[0:8]
