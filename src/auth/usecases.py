from uuid import uuid4

from src.auth.exceptions import LoginError, UsernameError
from src.auth.models import hash_password


def retrieve_user(repository, username: str):
    result = repository.get_by_username(username=username)
    return result


def is_logged_in(repository, username: str):
    result = repository.get_by_username(username=username)
    if result["token"] is not None:
        return True
    return False


def login(repository, username: str, password: str):
    account = repository.get_by_username(username=username)
    check_username(account=account, username=username, password=password)
    is_authenticated = check_password(account=account, password=password)
    if is_authenticated:
        return update_account_with_token(repository=repository, username=username)
    return False


def check_username(account, username, password):
    try:
        assert account is not None and account["username"] == username and password is not None
    except AssertionError:
        raise UsernameError


def check_password(account: dict, password: str):
    try:
        hashed = hash_password(password)
        assert account["password"] == hashed
        return True
    except AssertionError:
        raise LoginError


def update_account_with_token(repository, username: str):
    token = uuid4()
    repository.update_token(username=username, token=token)
    return token
