from src.common import sha256_hash_string


class Message:
    def __init__(self, sk: str, thread_id: str, author: str, content: str, posted_on: str, pk: int = None):
        self.pk = pk
        self.thread_id = thread_id
        self.posted_on = posted_on
        self.author = author
        self.content = content
        self.sk = sk

    @classmethod
    def create(cls, thread_id: str, author: str, content: str, posted_on: str):
        sk = get_key(f"{posted_on}-{content}")
        instance = cls(sk=sk, thread_id=thread_id, author=author, content=content, posted_on=posted_on)
        return instance


def get_key(chain):
    return sha256_hash_string(chain)[0:8]
