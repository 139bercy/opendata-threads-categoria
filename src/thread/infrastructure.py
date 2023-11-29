from src.config import postgres_client
from src.thread.gateways import AbstractThreadRepository
from src.thread.models import Message, Thread


class InMemoryThreadRepository(AbstractThreadRepository):
    def __init__(self, db):
        self.db = db

    def get_message_by_sk(self, sk: str) -> Message:
        return next((Message(**data) for data in self.db if data["sk"] == sk), None)

    def get_thread_by_sk(self, sk: str) -> Thread:
        return next((Thread(**data) for data in self.db if data["sk"] == sk), None)

    def create(self, message: Message) -> None:
        message.pk = len(self.db) + 1
        self.db.append(message.__dict__)

    def create_thread(self, thread: Thread) -> None:
        thread.pk = len(self.db) + 1
        self.db.append(thread.__dict__)


class PostgresThreadRepository(AbstractThreadRepository):
    client = postgres_client

    def get_message_by_sk(self, sk: str) -> Message:
        pass

    def get_thread_by_sk(self, sk: str) -> Thread:
        pass

    def create(self, message: Message) -> None:
        query = f"""INSERT INTO message(sk, thread_id, author, content, posted_on) VALUES ('{message.sk}', '{message.thread_id}','{message.author}', $${message.content}$$, '{message.posted_on}');"""
        postgres_client.add_one(query=query)

    def create_thread(self, thread: Thread) -> None:
        pass
