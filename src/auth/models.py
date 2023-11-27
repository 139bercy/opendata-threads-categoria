class Account:
    def __init__(self, username: str):
        self.username = username

    @classmethod
    def create(cls, username: str):
        instance = Account(username)
        return instance
