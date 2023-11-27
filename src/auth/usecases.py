from src.auth.models import hash_password


class LoginError(Exception):
    pass


def retrieve_user(repository, username: str):
    result = repository.get_by_username(username=username)
    return result


def login(repository, username: str, password: str):
    account = repository.get_by_username(username=username)
    try:
        assert account is not None and account["username"] == username
        hashed = hash_password(password)
        assert account["password"] == hashed
        return True
    except AssertionError:
        raise LoginError
