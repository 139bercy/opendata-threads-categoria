from src.infrastructure.client import postgres_client
from src.thread.gateways import AbstractThreadRepository
from src.thread.models import Message


class InMemoryThreadRepository(AbstractThreadRepository):
    def __init__(self, db):
        self.db = db

    def get_by_bk(self, bk: str) -> Message:
        return next((Message(**data) for data in self.db if data["bk"] == bk), None)

    def create(self, message: Message) -> None:
        message.pk = len(self.db) + 1
        self.db.append(message.__dict__)


class PostgresThreadRepository(AbstractThreadRepository):
    client = postgres_client

    def get_by_bk(self, bk: str) -> Message:
        pass

    def create(self, message: Message) -> None:
        query = f"""INSERT INTO message(bk, thread_id, author, content, posted_on) VALUES ('{message.bk}', '{message.thread_id}','{message.author}', $${message.content}$$, '{message.posted_on}');"""
        postgres_client.add_one(query=query)
