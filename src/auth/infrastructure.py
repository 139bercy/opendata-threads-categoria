from src.auth.models import Account
from src.infrastructure.client import postgres_client


class AccountInMemoryRepository:
    def __init__(self):
        self.db = [
            {
                "username": "jdoe",
                "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            }
        ]

    def get_by_username(self, username: str):
        return next((user for user in self.db if user["username"] == username), None)


class AccountPostgresqlRepository:
    client = postgres_client

    def get_by_username(self, username: str):
        query = f"""SELECT * FROM account acc WHERE acc.username = '{username}'"""
        return self.client.fetch_one(query=query)
