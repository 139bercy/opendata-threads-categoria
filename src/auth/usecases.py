from uuid import uuid4

from src.auth.exceptions import LoginError, UsernameError
from src.auth.models import Account
from src.common.utils import sha256_hash_string


def retrieve_account(repository, username: str):
    account = repository.get_by_username(username=username)
    return account


def is_logged_in(repository, username: str):
    account = repository.get_by_username(username=username)
    return account.is_logged_in


def login(repository, username: str, password: str):
    account = repository.get_by_username(username=username)
    check_username(account=account, username=username, password=password)
    is_authenticated = check_password(account=account, password=password)
    if is_authenticated:
        return update_account_with_token(repository=repository, username=username)


def check_username(account: Account, username: str, password: str):
    try:
        assert account is not None and account.username == username and password is not None
    except AssertionError:
        raise UsernameError


def check_password(account: Account, password: str):
    try:
        hashed = sha256_hash_string(password)
        assert account.password == hashed
        return True
    except AssertionError:
        raise LoginError


def update_account_with_token(repository, username: str):
    token = uuid4()
    repository.update_token(username=username, token=token)
    return token
