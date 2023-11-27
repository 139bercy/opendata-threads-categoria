from src.auth.models import hash_password
from uuid import uuid4


class LoginError(Exception):
    pass


def retrieve_user(repository, username: str):
    result = repository.get_by_username(username=username)
    return result


def login(repository, username: str, password: str):
    account = repository.get_by_username(username=username)
    is_authenticated = check_password(
        account=account, username=username, password=password
    )
    if is_authenticated:
        return update_account_with_token(repository=repository, username=username)
    return False


def check_password(account: dict, username: str, password: str):
    try:
        assert account is not None and account["username"] == username
        hashed = hash_password(password)
        assert account["password"] == hashed
        return True
    except AssertionError:
        raise LoginError


def update_account_with_token(repository, username: str):
    token = uuid4()
    repository.update_token(username=username, token=token)
    return token
