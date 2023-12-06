import base64
from uuid import uuid4, UUID

from auth.gateways import AbstractAccountRepository
from src.auth.exceptions import InvalidToken
from src.auth.exceptions import LoginError, UsernameError
from src.auth.models import Account
from src.common.utils import sha256_hash_string


def get_account_by_username(repository: AbstractAccountRepository, username: str):
    account = repository.get_by_username(username=username)
    return account


def user_is_logged_in(repository: AbstractAccountRepository, username: str) -> bool:
    account = repository.get_by_username(username=username)
    return account.is_logged_in


def login(repository: AbstractAccountRepository, username: str, password: str) -> str:
    """:returns base64 encoded string if authentication is successful"""
    account = repository.get_by_username(username=username)
    check_username(account=account, username=username, password=password)
    is_authenticated = check_password(account=account, password=password)
    if is_authenticated:
        token = uuid4()
        cookie = encode_token(username=username, token=token)
        update_account_with_token(repository=repository, username=username, token=token)
        return cookie


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


def update_account_with_token(repository: AbstractAccountRepository, username: str, token: UUID):
    """Update account data with created token"""
    repository.update_token(username=username, token=token)
    return token


def encode_token(username: str, token: UUID):
    """Create session cookie"""
    userpass = f"{username}:{token}"
    result = base64.b64encode(userpass.encode()).decode()
    return result


def check_token(repository, encoded_token):
    """Decode and compare token to registered account token"""
    username, token = decode_token(encoded_token)
    account = repository.get_by_username(username=username)
    if not account.token_is_valid(token):
        raise InvalidToken
    return True


def decode_token(encoded_token):
    username, token = tuple(base64.b64decode(encoded_token).decode("utf-8").split(":"))
    return username, token
