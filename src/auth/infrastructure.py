from uuid import UUID
from src.infrastructure.client import postgres_client


class AccountInMemoryRepository:
    def __init__(self):
        self.db = [
            {
                "username": "jdoe",
                "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "token": None,
            },
            {
                "username": "jsmith",
                "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "token": UUID("d6a813de-73c1-4328-aa55-0ac1a0120b20"),
            },
        ]

    def get_by_username(self, username: str):
        return next((user for user in self.db if user["username"] == username), None)

    def update_token(self, username, token):
        for i, account in enumerate(self.db):
            if account["username"] == username:
                account["token"] = token
                # self.db[i] = account


class AccountPostgresqlRepository:
    client = postgres_client

    def get_by_username(self, username: str):
        query = f"""SELECT * FROM account acc WHERE acc.username = '{username}';"""
        return self.client.fetch_one(query=query)

    def update_token(self, username, token):
        if token:
            query = f"""UPDATE account acc SET token = '{token}' WHERE acc.username = '{username}';"""
        else:
            query = f"""UPDATE account acc SET token = null WHERE acc.username = '{username}';"""
        self.client.update(query)
