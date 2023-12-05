import base64
from uuid import uuid4, UUID

from src.auth.exceptions import LoginError, UsernameError
from src.auth.models import Account
from src.common.utils import sha256_hash_string


class InvalidToken(Exception):
    pass


def retrieve_account(repository, username: str):
    account = repository.get_by_username(username=username)
    return account


def is_logged_in(repository, username: str) -> bool:
    account = repository.get_by_username(username=username)
    return account.is_logged_in


def login(repository, username: str, password: str) -> str:
    """:returns base64 encoded string if authentication is successful"""
    account = repository.get_by_username(username=username)
    check_username(account=account, username=username, password=password)
    is_authenticated = check_password(account=account, password=password)
    if is_authenticated:
        token = uuid4()
        session_token = encode_token(username=username, token=token)
        update_account_with_token(repository=repository, username=username, token=token)
        return session_token


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


def update_account_with_token(repository, username: str, token: UUID):
    repository.update_token(username=username, token=token)
    return token


def encode_token(username, token):
    userpass = f"{username}:{token}"
    result = base64.b64encode(userpass.encode()).decode()
    return result


def check_token(repository, encoded_token):
    username, token = tuple(base64.b64decode(encoded_token).decode("utf-8").split(":"))
    account = repository.get_by_username(username=username)
    if not account.token_is_valid(token):
        raise InvalidToken
    return True
