from src.thread.models import Message


class InMemoryThreadRepository:
    def __init__(self):
        self.db = []

    def get_by_bk(self, bk: str):
        return next((Message(**message) for message in self.db if message["bk"] == bk), None)

    def create(self, message):
        self.db.append(message.__dict__)
