import pytest
import os 
import json

from requests_mock import Mocker

from src.core.models import Message, Thread
from src.core.usecases import create_message, create_thread
from get_ressourcesVrai import APIDataFetcher

@pytest.fixture
def api_sources():
    return [
        {"url": "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"}
        # Add more sources if needed
    ]

def test_create_instance(api_sources):
    #Arrange
    """api_sources = [
        {
            "url": "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
         }

    ]"""
    #organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
    #Act
    api = APIDataFetcher(api_sources)
    #Assert 
    assert isinstance(api, APIDataFetcher) 



def test_save_data_to_json(api_sources, tmp_path):
    """tmp_path est un objet Path qui pointe vers un répertoire temporaire spécifique à chaque test. 
       On peut l'utiliser pour créer des fichiers temporaires, des répertoires temporaires, etc.
       Il sera automatiquement nettoyé à la fin de chaque test."""
    api= APIDataFetcher(api_sources, data_folder=tmp_path)
    resource = "datasetstest"

    # Simulate fetching and processing data
    data = {"key": "value"}
    api.save_data_to_json(resource, data)

    # Test if the file is created
    filename = f"{resource}.json"
    assert os.path.exists(tmp_path / filename)

    # Test if the file contains data
    file_path = tmp_path / filename
    with open(file_path, "r") as file:
        file_contents = json.load(file)
    assert file_contents == data

    # Clean up: Remove the test file after the test
    os.remove(file_path)


