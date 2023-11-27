from src.auth.models import Account
from src.infrastructure.client import postgres_client


class AccountInMemoryRepository:
    def __init__(self):
        self.db = [Account(username="jdoe")]

    def get_by_username(self, username: str):
        return next((user for user in self.db if user.username == username))


class AccountPostgresqlRepository:
    client = postgres_client

    def get_by_username(self, username: str):
        query = f"""SELECT * FROM account acc WHERE acc.username = '{username}'"""
        return self.client.fetch_one(query=query)
