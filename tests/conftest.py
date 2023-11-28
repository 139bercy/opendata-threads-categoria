import os

import pytest

from src.infrastructure.client import postgres_client

os.environ["APP_ENV"] = "test"
os.environ["DB_NAME"] = "app_db_test"
os.environ["DB_PORT"] = "5433"


def concatenate_files(file_paths):
    concatenated_content = ""
    for file_path in file_paths:
        with open(file_path, "r") as file:
            content = file.read()
            concatenated_content += content
    return concatenated_content


@pytest.fixture
def db_fixture():
    file_paths = ["ci/volumes/schema.sql", "tests/fixtures.sql"]
    result = concatenate_files(file_paths)
    postgres_client.execute(result)
