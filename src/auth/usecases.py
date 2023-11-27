from src.auth.models import hash_password


class UserDoesNotExistsError(Exception):
    pass


def retrieve_user(repository, username):
    result = repository.get_by_username(username=username)
    return result


def login(repository, username: str, password: str):
    account = repository.get_by_username(username=username)
    if account is None:
        raise UserDoesNotExistsError
    hashed = hash_password(password)
    try:
        assert account["username"] == username and account["password"] == hashed
        return True
    except AssertionError:
        return False
