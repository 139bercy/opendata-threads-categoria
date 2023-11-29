from __future__ import annotations
from src.common.utils import sha256_hash_string


class Message:
    def __init__(self, sk: str, thread_id: str, author: str, content: str, posted_on: str, pk: int = None):
        self.pk = pk
        self.thread_id = thread_id
        self.posted_on = posted_on
        self.author = author
        self.content = content
        self.sk = sk

    @classmethod
    def create(cls, thread_id: str, author: str, content: str, posted_on: str) -> Message:
        sk = get_key(f"{posted_on}-{content}")
        instance = cls(sk=sk, thread_id=thread_id, author=author, content=content, posted_on=posted_on)
        return instance


class Thread:
    def __init__(self, sk: str, title: str, pk: int = None) -> None:
        self.pk = pk
        self.sk = sk
        self.title = title

    @classmethod
    def create(cls, title: str) -> Thread:
        sk = get_key(f"{title}")
        instance = cls(sk=sk, title=title)
        return instance


def get_key(chain):
    return sha256_hash_string(chain)[0:8]
