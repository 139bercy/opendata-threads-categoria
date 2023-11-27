def retrieve_user(repository, username):
    result = repository.get_by_username(username=username)
    return result
