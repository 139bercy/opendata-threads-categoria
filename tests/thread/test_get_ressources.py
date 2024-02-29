from src.core.models import Message, Thread
from src.core.usecases import create_message, create_thread
from get_resourcesMOD import APIDataFetcher


def test_create_instance():
    #Arrange
    base_url = "https://www.data.gouv.fr/api/1/organizations"
    organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
    #Act
    api = APIDataFetcher(base_url, organization)
    #Assert 
    assert isinstance(api, APIDataFetcher) 