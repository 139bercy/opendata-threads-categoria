import os

import pytest

from src.config import postgres_client

os.environ["APP_ENV"] = "test"
os.environ["DB_NAME"] = "app_db_test"
os.environ["DB_PORT"] = "5433"


@pytest.fixture
def db_fixture():
    """Prépare la base de données de test à recevoir les tests d'intégration."""
    file_paths = ["ci/volumes/schema.sql", "tests/fixtures.sql"]
    result = concatenate_files(file_paths)
    postgres_client.execute(result)


def concatenate_files(file_paths):
    concatenated_content = ""
    for file_path in file_paths:
        with open(file_path, "r") as file:
            content = file.read()
            concatenated_content += content
    return concatenated_content
