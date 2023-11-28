from uuid import UUID

from src.auth.models import Account
from src.infrastructure.client import postgres_client


class AccountInMemoryRepository:
    def __init__(self):
        self.db = [
            {
                "pk": 1,
                "sk": UUID("fe06e149-0aeb-44a3-a0e5-e8f9dcbbfe79"),
                "username": "jdoe",
                "email": "john.doe@example.com",
                "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "token": None,
            },
            {
                "pk": 2,
                "sk": UUID("03949324-f5f9-424b-9d96-852c0916ca22"),
                "username": "jsmith",
                "email": "john.smith@example.com",
                "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "token": UUID("d6a813de-73c1-4328-aa55-0ac1a0120b20"),
            },
        ]

    def get_by_username(self, username: str):
        return next((Account(**data) for data in self.db if data["username"] == username), None)

    def update_token(self, username, token):
        for i, account in enumerate(self.db):
            if account["username"] == username:
                account["token"] = token
                # self.db[i] = account


class AccountPostgresqlRepository:
    client = postgres_client

    def get_by_username(self, username: str):
        query = (
            f"""SELECT pk, sk, username, email, password, token  FROM account acc WHERE acc.username = '{username}';"""
        )
        data = self.client.fetch_one(query=query)
        return Account(**data)

    def update_token(self, username, token):
        if token:
            query = f"""UPDATE account acc SET token = '{token}' WHERE acc.username = '{username}';"""
        else:
            query = f"""UPDATE account acc SET token = null WHERE acc.username = '{username}';"""
        self.client.update(query)
