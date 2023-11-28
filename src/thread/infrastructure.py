from src.thread.models import Message


class InMemoryThreadRepository:
    def __init__(self, db):
        self.db = db

    def get_by_bk(self, bk: str):
        return next((Message(**data) for data in self.db if data["bk"] == bk), None)

    def create(self, message):
        message.pk = len(self.db) + 1
        self.db.append(message.__dict__)
