import json
import requests
import pytest
import psycopg2
import os
import dotenv

from dataclasses import dataclass
from src.core.models import Message, Thread, Dataset

from src.common.infrastructure import PostgresClient
from src.core.infrastructure import PostgresThreadRepository

dotenv.load_dotenv()

@dataclass
class DataGouvDatasetDTO:
    buid: str
    title: str
    description: str = None
    # organization: str
    # url: str
    # creation_date: str
    # discussions_count: int
    # followers_count: int
    # reuses_count: int
    # views_count: int
    # remote_id_data_eco: str
    # slug_data_gouv: str
    # created_dataset: str

"""@dataclass
class Discussion:
    dataset_id: str
    discussion_id: str
    author: str
    content: str
    mesage_posted_on: str
    discussion_created: str
    discussion_closed: str
    title: str"""

@pytest.fixture
def postgres_thread_repository():
    # Create a PostgresClient using the environment variables
    postgres_client = PostgresClient(
        dbname=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD"),
    )

    # Initialize the PostgresThreadRepository using the PostgresClient
    repository = PostgresThreadRepository(postgres_client)

    # Return the repository for the tests
    return repository

"""def get_datasets_from_data_gouv_api():    
    base_url = "https://www.data.gouv.fr/api/1/organizations"
    organization = "/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"

    url = f"{base_url}{organization}/datasets"
    response = requests.get(url=url)
    print(response.status_code)

    with open("tmp.json", "w") as file:
        data = json.loads(response.text)
        json.dump(data, file, indent=2, ensure_ascii=False)
    return data
"""


def get_all_datasets_from_data_gouv_api(base_url, organization, resource):

    datasets = []
    page = 1

    while True:
        url = f"{base_url}/{organization}/{resource}?page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error fetching data for page {page}. Status code: {response.status_code}")
            break

        data = response.json()

        if not data["data"]:
            break

        # Ajouter les données de toutes les pages dans la même liste( j'ai choisi de ne pas prendre en compte l'argument "data" retourné par l'API)
        datasets.extend(data["data"])

        page += 1

    return datasets


def save_datasets_to_json(datasets, filename="tests/fixtures/dg-datasets.json"):
    with open(filename, "w") as file:
        json.dump(datasets, file, indent=2, ensure_ascii=False)


organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
resource = "datasets"

def process_data(base_url, organization, resource):
    # Appel à la fonction pour récupérer et enregistrer les données
    all_datasets = get_all_datasets_from_data_gouv_api(base_url, organization, resource)
    save_datasets_to_json(all_datasets)


#process_data(base_url, organization, resource)


def test_get_a_dataset_from_data_gouv():
    # Arrange
    with open("tests/fixtures/dg-datasets.json", "r")  as file:
        #data = json.load(file)["data"][0]
        data = json.load(file)[0]
    # Act
    dataset = DataGouvDatasetDTO(
        buid="azerty", 
        title=data["title"], 
        description=data["description"]
    )
    # Assert
    assert dataset.title == "Tableaux Statistiques de la Direction Générale des Finances Publiques (DGFiP)"
    assert len(dataset.description) >= 150


class InMemoryDatasetRepository:
    def __init__(self, db: list) -> None:
        self.db = db

    def add(self, dataset: DataGouvDatasetDTO):
        self.db.append(dataset)

    def add_all(self, datasets: list):
        self.db.extend(datasets)

    def get(self, dataset_id):
        return next((ds for ds in self.db if ds.buid == dataset_id), None)
    
    def clear(self):
        self.db = []


def test_append_a_dataset_to_database():
    # Arrange
    dataset = DataGouvDatasetDTO("azerty", "title", "description")
    repository = InMemoryDatasetRepository(db=[])
    # Act
    repository.add(dataset)
    # Assert
    assert len(repository.db) == 1


def test_get_a_dataset_from_repository():
    # Arrange
    dataset = DataGouvDatasetDTO(buid="azerty", title="title", description="description")
    repository = InMemoryDatasetRepository(db=[dataset])
    dataset_id = "azerty"
    # Act
    result = repository.get(dataset_id)
    # Assert
    assert result == dataset

"""def test_get_dataset_with_wrong_id_from_repository_should_return_none():
    # Arrange
    dataset = DataGouvDatasetDTO("azerty", "title", "description")
    repository = InMemoryDatasetRepository(db=[dataset])
    dataset_id = "azerty"
    # Act
    result = repository.get(dataset_id)
    # Assert
    assert 0 == 1"""

"""
Cherche les datasets à partir de l'API data.gouv (URL, dict python)
Créer le modèle de données
Ajoute les nouveaux datasets à la base de données
"""

def test_get_datasets_from_data_gouv():    
    # Arrange
    with open("tests/fixtures/dg-datasets.json", "r")  as file:
        dataset_count = 0
        data = json.load(file)
    #Act
        datasets_list = []

        for dataset in data:
            #print('\n')

            # Créer une instance de DataGouvDatasetDTO pour chaque ensemble de données
            current_dataset = DataGouvDatasetDTO(
                buid="azerty", 
                title=dataset["title"],
                #description=dataset["description"]
            )
            
            # Ajouter l'instance à la liste
            datasets_list.append(current_dataset)

            # Imprimer les valeurs pour vérification
            # Accédez aux champs spécifiés
            #print("title_dataset:", dataset["title"])
            #print("description_dataset:", dataset["description"].replace('\n', ' '))
            #print("organization:", dataset["organization"]["name"])
            #print("url_dataset:", dataset["page"])
            #print("nb_discussions:", dataset["metrics"]["discussions"])
            #print("nb_followers:", dataset["metrics"]["followers"])
            #print("nb_reuses:", dataset["metrics"]["reuses"])
            #print("nb_views:", dataset["metrics"]["views"])
            #print("remote_id_dataEco:", dataset["harvest"]["remote_id"] if dataset['harvest'] and 'remote_id' in dataset['harvest'] else None)
            #print("slug_dataGouv:", dataset["slug"]) #slug sur data.gouv mais sur data.eco, l'équivalent est 'remote_id'
            #print("created_dataset:", dataset["created_at"])
            ##"last_update_dataset": dataset_updated_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            
            dataset_count += 1
            
        # Imprimez le nombre total de données récupérées
        #print(f"\nTotal datasets recupérés: {dataset_count}")
        #print(datasets_list)
        #print(f"len de datasets_list :{len(datasets_list)}")

    # Assert
    assert dataset_count == len(datasets_list)


def test_append_datasets_to_database():
    # Arrange
    datasets = [
        DataGouvDatasetDTO("azerty", "title1", "description1"),
        DataGouvDatasetDTO("qwerty", "title2", "description2"),
    ]
    repository = InMemoryDatasetRepository(db=[])

    # Act
    repository.add_all(datasets)

    # Assert
    assert len(repository.db) == len(datasets)

    # Additional assertions if needed
    for dataset in datasets:
        result = repository.get(dataset.buid)
        assert result == dataset


def test_get_datasets_from_repository():
    # Arrange
    datasets = [
        DataGouvDatasetDTO(buid="azerty", title="title1", description="description1"),
        DataGouvDatasetDTO(buid="qwerty", title="title2", description="description2"),
    ]
    repository = InMemoryDatasetRepository(db=datasets)

    # Act and Assert
    for dataset in datasets:
        result = repository.get(dataset.buid)
        assert result == dataset


def test_clear_database():
    # Arrange
    datasets = [
        DataGouvDatasetDTO("azerty", "title1", "description1"),
        DataGouvDatasetDTO("qwerty", "title2", "description2"),
    ]
    repository = InMemoryDatasetRepository(db=datasets)

    # Act
    repository.clear()

    # Assert
    assert len(repository.db) == 0


def create_table_dataset_in_database_postgres():
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            port=os.getenv("DB_PORT"),
            password=os.getenv("DB_PASSWORD"),
        )

        # curseur pour exécuter les commandes SQL
        cursor = connection.cursor()

        # Création de la table dataset
        create_table_dataset = """
        CREATE TABLE IF NOT EXISTS dataset (
            buid        TEXT PRIMARY KEY NOT NULL,
            title       TEXT NOT NULL,
            description TEXT
        );
        """

        # Exécutez la commande SQL
        cursor.execute(create_table_dataset)

        # Validez les modifications dans la base de données
        connection.commit()

        # Fermez le curseur et la connexion
        cursor.close()
        connection.close()

        print("Table dataset created successfully in PostgreSQL.")

    except Exception as e:
        print(f"Error creating table dataset: {e}")

# Appelez la fonction pour créer la table dataset
create_table_dataset_in_database_postgres()

def test_create_table_dataset_in_database_postgres():
    
    # Appelez la fonction pour créer la table dataset
    create_table_dataset_in_database_postgres()
    
    # Connectez-vous à la base de données PostgreSQL pour vérifier la table
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD"),
    )

    # Créez un objet curseur pour exécuter des commandes SQL
    cursor = connection.cursor()

    # Exécutez une requête pour vérifier si la table existe
    cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'dataset';")
    result = cursor.fetchone()

    # Fermez le curseur et la connexion
    cursor.close()
    connection.close()

    # Assert pour vérifier si la table existe
    assert result is not None


def test_append_a_dataset_to_postgres_database(postgres_thread_repository):
    # Arrange
    dataset = Dataset(buid="azerty", title="title", description="description")

    # Act
    postgres_thread_repository.add_dataset(dataset)
    print("Dataset added to the database")

    # Assert
    result = postgres_thread_repository.get_dataset_by_buid(dataset.buid)
    #assert result == dataset
    assert result is not None


if __name__ == "__main__":

    base_url = "https://www.data.gouv.fr/api/1/organizations"
    organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
    resource = "datasets"

    process_data(base_url, organization, resource)