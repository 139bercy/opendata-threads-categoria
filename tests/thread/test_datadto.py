import json
import requests
import pytest
import os

from bs4 import BeautifulSoup
from dataclasses import dataclass
from src.core.gateways import AbstractDatasetRepository
from src.common.utils import sha256_hash_string
from src.config import postgres_client
from tests.conftest import db_fixture


def get_key(chain):
    """
    Utiliser les 8 premiers caractères d'un hash est à ce stade suffisamment discriminant pour éviter les collisions.
    """
    return sha256_hash_string(chain)[0:8]


################## DATASET ####################################################################################


@dataclass
class Dataset:
    buid: str = None  # id générée manuellement
    dataset_uid: str = None
    dataset_id: str = None
    title: str = None
    description: str = None
    publisher: str = None
    # published: bool = None
    created: str = None
    updated: str = None
    # restricted: bool = None
    # organization: str
    # url: str
    # creation_date: str
    # discussions_count: int
    # followers_count: int
    # reuses_count: int
    # views_count: int
    # remote_id_data_eco: str = None
    # slug_data_gouv: str = None
    # created_dataset: str

    # Opérations CRUD : créer, récupérer, mettre à jour et supprimer un dataset dans la classe Dataset.
    @classmethod
    def create(
        cls, buid: str, dataset_uid: str, dataset_id: str, title: str, description: str, publisher: str, created: str, updated: str
    ) -> "Dataset":
        """
        Crée une instance de Dataset avec une buid calculée à partir d'un hash du slug.
        """
        #buid = get_key(f"{title}")  # VOIR pour remplacer buid par f"{slug}"", trouver une id_unique pour le dataset
        instance = cls(
            buid = buid,
            dataset_uid = dataset_uid,
            dataset_id = dataset_id,
            title = title,
            description = description,
            publisher = publisher,
            created = created,
            updated = updated,
        )
        return instance

    def update(self, title: str, description: str) -> None:
        if title:
            self.title = title
            self.buid = get_key(self.title)
        if description:
            self.description = description


class InMemoryDatasetRepository(AbstractDatasetRepository):
    def __init__(self, db):
        self.db = db

    def create_dataset(self, dataset: Dataset) -> None:
        dataset.pk = len(self.db) + 1
        self.db.append(dataset.__dict__)

    """def get_dataset_by_buid(self, buid: str) -> Dataset:
        return next((Dataset(**data) for data in self.db if data["buid"] == buid), None)"""

    def get_dataset_by_buid(self, buid: str) -> Dataset:
        for data in self.db:
            if data.buid == buid:
                return data
        return None


"""class InMemoryDatasetRepository:
    def __init__(self, db: list) -> None:
        self.db = db

    def add(self, dataset: Dataset):
        self.db.append(dataset)

    def add_all(self, datasets: list):
        self.db.extend(datasets)

    def get(self, dataset_id):
        return next((ds for ds in self.db if ds.buid == dataset_id), None)
    
    def clear(self):
        self.db = []"""


class PostgresDatasetRepository(AbstractDatasetRepository):
    def __init__(self, postgres_client):
        self.postgres_client = postgres_client

    def create_dataset(self, dataset: Dataset) -> None:
        query = f"""
            INSERT INTO dataset(buid, dataset_uid, dataset_id, title, description, publisher, created, updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            dataset.buid,
            dataset.dataset_uid,
            dataset.dataset_id,
            dataset.title,
            dataset.description,
            dataset.publisher,
            dataset.created,
            dataset.updated,
        )
        postgres_client.add_one(query, params=values)

    def get_dataset_by_buid(self, buid: str) -> Dataset:
        query = """
            SELECT buid, dataset_uid, dataset_id, title, description, publisher, created, updated
            FROM dataset
            WHERE buid = %s;
        """
        result = postgres_client.fetch_one(
            query, params=(buid,)
        )  # self.postgres_client.fetch_one(query, params=(buid,))
        if result:
            return Dataset(*result)
        return None

    def delete(self, buid: str) -> None:
        """
        Supprime le dataset de la base de données en utilisant le buid comme identifiant.
        """
        query = """
            DELETE FROM dataset
            WHERE buid = %s;
        """
        postgres_client.execute(query, (buid,))


################## DATA GOUV DTO ####################################################################################


@dataclass
class DataGouvDatasetDTO:
    buid: str
    title: str
    description: str
    # organization: str
    # url: str
    # creation_date: str
    # discussions_count: int
    # followers_count: int
    # reuses_count: int
    # views_count: int
    # remote_id_data_eco: str = None
    # slug_data_gouv: str = None
    # created_dataset: str

    @staticmethod
    def fetch_data_from_datagouv(base_url: str, organization: str, resource: str, page: int = 1) -> dict:
        """
        Récupère les données brutes à partir de l'API de data.gouv.fr
        """
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

            # J'ai fait le choix de ne pas prendre en compte l'argument "data" retourné par l'API
            datasets.extend(data["data"])

            page += 1

        return datasets

    @classmethod
    def save_data_from_datagouv_to_json(cls, filename: str, datasets: list) -> None:
        """
        Enregistre les données brutes récupérées de l'API dans un fichier JSON.
        """
        with open(filename, "w") as file:
            json.dump(datasets, file, indent=2, ensure_ascii=False)
    
    @classmethod
    def retrieve_and_convert_data_to_datagouv_dto(cls, datasets) -> list:
        """
        Méthode qui utilise les données brutes récupérées de l'API,
        puis elle les convertit en objets de classe DataGouvDatasetDTO.
        Elle est responsable de convertir les données brutes en objets DTO.
        """
        dtos = []
        for data in datasets:
            buid = get_key(data["title"])
            title = data["title"]
            description = data["description"]
            #remote_id = data["harvest"]["remote_id"]
            #dataset_id = data["id"]
            #nb_discussions = data["metrics"]["discussions"]
            #nb_followers = data["metrics"]["followers"]
            #nb_reuses = data["metrics"]["reuses"]
            #nb_views = data["metrics"]["views"]
            #quality_score = data["quality"]["score"]
            #slug = data["slug"]

            # Create a DataGouvDatasetDTO object with the extracted data
            dto = cls(
                buid=buid,
                title=title,
                description=description,
                #remote_id=remote_id,
                #dataset_id=dataset_id,
                #nb_discussions=nb_discussions,
                #nb_followers=nb_followers,
                #nb_reuses=nb_reuses,
                #nb_views=nb_views,
                #quality_score=quality_score,
                #slug=slug
            )
            dtos.append(dto)
        return dtos


    def convert_datagouv_dto_to_dataset(self) -> Dataset:
        """
        Cette méthode convertit un objet DTO (Data Transfer Object) en un objet de classe Dataset.
        """
        #return Dataset(buid=self.buid, title=self.title, description=self.description)
        return Dataset(buid=self.buid, title=self.title, description=self.description)


################## DATA ECO DTO ####################################################################################


@dataclass
class DataEcoDatasetDTO:
    buid: str # business id générée manuellement
    dataset_id: str
    dataset_uid: str
    title: str
    description: str
    publisher: str
    # published: bool
    created: str
    updated: str
    # restricted: bool

    @staticmethod
    def fetch_data_from_dataeco() -> list:
        """
        Récupère les données brutes à partir de l'API de data.economie.gouv.fr
        """
        base_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"
        limit = 100  # Limite de pagination par défaut
        offset = 0  # Offset initial

        datasets = []

        while True:
            # Faites une requête pour récupérer une page de données
            response = requests.get(base_url, params={"limit": limit, "offset": offset})
            data = response.json()["results"]

            # Ajoutez les données de cette page à la liste des données
            datasets.extend(data)

            # Passez à la page suivante
            offset += limit

            # Vérifiez s'il y a plus de données à récupérer
            if not data or len(data) < limit:
                break

        return datasets
    
    @staticmethod
    def clean_html_tags(html_text: str) -> str:
        """Clean HTML tags from a given HTML text."""
        if html_text is None:
            return ""
        soup = BeautifulSoup(html_text, "html.parser")
        return soup.get_text()

    @classmethod
    def save_data_from_dataeco_to_json(cls, filename: str, datasets: list) -> None:
        """
        Enregistre les données brutes récupérées de l'API dans un fichier JSON.
        """
        with open(filename, "w") as file:
            json.dump(datasets, file, indent=2, ensure_ascii=False)

    @classmethod
    def retrieve_and_convert_data_to_dataeco_dto(cls, datasets) -> list:
        """
        Méthode qui utilise la méthode fetch_data pour récupérer les données brutes de l'API,
        puis elle les convertit en objets de classe DataEcoDatasetDTO.
        Elle est responsable de convertir les données brutes en objets DTO.
        """
        dtos = []
        for data in datasets:
            buid = get_key(data["metas"]["default"]["title"])
            dataset_id = data["dataset_id"]
            dataset_uid = data["dataset_uid"]
            title = data["metas"]["default"]["title"]
            # Extracting description and cleaning HTML tags
            description_html = data["metas"]["default"]["description"]
            description = cls.clean_html_tags(description_html)
            publisher = data["metas"]["default"]["publisher"]
            created = data["metas"]["custom"]["date-de-creation"]
            updated = data["metas"]["default"]["modified"]
            
            # Créez un objet DataEcoDatasetDTO avec les données extraites
            dto = cls(
                buid = buid,
                dataset_id = dataset_id,
                dataset_uid = dataset_uid,
                title = title,
                description = description,
                publisher = publisher,
                created = created,
                updated = updated
                # restricted = data['restricted']
            )
            dtos.append(dto)
        return dtos

    def convert_dataeco_dto_to_dataset(self) -> Dataset:
        """
        Cette méthode convertit un objet DTO (Data Transfer Object) en un objet de classe Dataset.
        """
        return Dataset(
            buid = self.buid,
            dataset_uid = self.dataset_uid,
            dataset_id = self.dataset_id,
            title = self.title,
            description = self.description,
            publisher = self.publisher,
            created = self.created,
            updated = self.updated,
        )


################## TESTS DATA GOUV ####################################################################################


# Tests pour DataGouvDatasetDTO
def test_get_a_dataset_from_data_gouv():
    # Arrange
    """# Fetch data from data.gouv API
    base_url = "https://www.data.gouv.fr/api/1/organizations"
    organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
    resource = "datasets"
    data_gouv_datasets = DataGouvDatasetDTO.fetch_data_from_datagouv(base_url, organization, resource)
    # Save data to a JSON file
    DataGouvDatasetDTO.save_data_from_datagouv_to_json("tests/fixtures/testgouv.json", data_gouv_datasets)"""

    with open("tests/fixtures/testgouv.json", "r") as file:
        # data = json.load(file)["data"][0]
        data = json.load(file)[0]
    # Act
    expected_data = DataGouvDatasetDTO(buid="azerty", title=data["title"], description=data["description"])
    # Assert
    assert expected_data.title == "Tableaux Statistiques de la Direction Générale des Finances Publiques (DGFiP)"
    assert len(expected_data.description) >= 150


def test_retrieve_and_convert_datagouv_to_dto():
    # Arrange
    datasets = [
        {"title": "Title 1", "description": "Description 1"},
        {"title": "Title 2", "description": "Description 2"},
    ]

    # Act
    dtos = DataGouvDatasetDTO.retrieve_and_convert_data_to_datagouv_dto(datasets)

    # Assert
    assert isinstance(dtos, list)
    assert len(dtos) == 2
    for dto in dtos:
        assert isinstance(dto, DataGouvDatasetDTO)
        assert dto.buid == get_key(dto.title)
        print(f"{dto.title} and {dto.buid}")


def test_convert_datagouv_dto_to_dataset():
    # Arrange
    dto = DataGouvDatasetDTO(buid="buid", title="title", description="description")
    # Act
    dataset = dto.convert_datagouv_dto_to_dataset()
    # Assert
    assert isinstance(dataset, Dataset)
    assert dataset.buid == "buid"
    assert dataset.title == "title"
    assert dataset.description == "description"


################## TESTS DATA ECO ####################################################################################

# Tests pour DataEcoDatasetDTO
def test_get_a_dataset_from_data_eco():
    # Arrange
    # Fetch data from data.economie API
    #data_eco_datasets = DataEcoDatasetDTO.fetch_data_from_dataeco()
    # Save data to a JSON file
    #DataEcoDatasetDTO.save_data_from_dataeco_to_json("tests/fixtures/testeco.json", data_eco_datasets)

    with open("tests/fixtures/testeco.json", "r") as file:
        data = json.load(file)[0]
        # data = json.load(file)["results"][0]
    # Act
    expected_data = DataEcoDatasetDTO(
        dataset_id=data["dataset_id"],
        dataset_uid=data["dataset_uid"],
        title=data["metas"]["default"]["title"],
        description=data["metas"]["default"]["description"],
        publisher=data["metas"]["default"]["publisher"],
        # published = data["published"],
        # editor = data["metas"]["custom"]["editeur"],
        created=data["metas"]["custom"]["date-de-creation"],
        updated=data["metas"]["default"]["modified"],
        # restricted=data["restricted"]
    )
    # Assert
    assert expected_data.dataset_id == "lfi-2012-dotation-ccf-titre-2-et-hors-titre-2-par-mission"
    assert expected_data.title == "Loi de finances initiale 2012, dotation comptes de concours financiers (CCF) titre 2 et hors titre 2 (H2 et HT2)  par mission (LFI 2012)"
    assert len(expected_data.description) >= 100


def test_retrieve_and_convert_data_to_dataeco_dto():
    # Arrange
    datasets = [
        {
            "dataset_id": "1",
            "dataset_uid": "azerty",
            "metas": {
                "default": {
                    "title": "Title 1",
                    "description": "Description 1",
                    "publisher": "Publisher 1",
                    "modified": "2023-01-01T00:00:00Z"
                },
                "custom": {
                    "date-de-creation": "2023-01-01T00:00:00Z"
                }
            }
        },
        {
            "dataset_id": "2",
            "dataset_uid": "qwerty",
            "metas": {
                "default": {
                    "title": "Title 2",
                    "description": "Description 2",
                    "publisher": "Publisher 2",
                    "modified": "2023-01-02T00:00:00Z"
                },
                "custom": {
                    "date-de-creation": "2023-01-02T00:00:00Z"
                }
            }
        }
    ]

    # Act
    # datasets = DataGouvDatasetDTO.fetch_data(base_url, organization, resource)  # VOIR POUR BUID A GENERER !!!!!!!!!!!!!!!!!!!!!!
    dtos = DataEcoDatasetDTO.retrieve_and_convert_data_to_dataeco_dto(datasets)
    # Assert
    assert isinstance(dtos, list)
    assert len(dtos) == 2
    assert dtos[0].dataset_uid == "azerty"
    for dto in dtos:
        assert isinstance(dto, DataEcoDatasetDTO)
        assert dto.dataset_id in ["1", "2"]
        assert dto.dataset_uid in ["azerty", "qwerty"]


def test_convert_dataeco_dto_to_dataset():
    # Arrange
    dto = DataEcoDatasetDTO(
        dataset_id="dataset_id",
        dataset_uid="azerty",
        title="title",
        description="description",
        publisher="publisher",
        created="created",
        updated="updated",
    )
    # Act
    dataset = dto.convert_dataeco_dto_to_dataset()
    # Assert
    assert isinstance(dataset, Dataset)
    assert dataset.dataset_id == "dataset_id"
    assert dataset.dataset_uid == "azerty"
    assert dataset.title == "title"
    assert dataset.description == "description"
    assert dataset.publisher == "publisher"
    assert dataset.created == "created"
    assert dataset.updated == "updated"


################## TESTS DATASET ####################################################################################


def test_create_dataset():
    # Arrange
    buid = "buid"
    dataset_uid = "azerty"
    dataset_id = "dataset_id"
    title = "Test Dataset"
    description = "This is a test dataset"
    publisher = "Test Publisher"
    created = "2023-01-01"
    updated = "2023-01-02"

    # Act
    dataset = Dataset.create(buid, dataset_uid, dataset_id, title, description, publisher, created, updated)

    # Assert
    assert isinstance(dataset, Dataset)
    assert dataset.buid is not None
    assert dataset.dataset_uid == dataset_uid
    assert dataset.dataset_id == dataset_id
    assert dataset.title == title
    assert dataset.description == description
    assert dataset.publisher == publisher
    assert dataset.created == created
    assert dataset.updated == updated


def test_update_dataset():
    # Arrange
    dataset = Dataset(
        buid="buid",
        dataset_uid="azerty",
        dataset_id="dataset_id",
        title="title",
        description="description",
        publisher="publisher",
        created="created",
        updated="updated",
    )

    # Act
    dataset.update(title="Updated Title", description="Updated Description")

    # Assert
    assert dataset.title == "Updated Title"
    assert dataset.description == "Updated Description"


"""def test_delete_Postgres_dataset():
    # Arrange
    dataset = Repository.create(dataset_uid="azerty", dataset_id="dataset_id", title="title", description="description", publisher="publisher", created="created", updated="updated")

    # Act
    dataset.delete()

    # Assert
    assert dataset.buid is None
    assert dataset.title is None
    assert dataset.description is None
    assert dataset.publisher is None
    assert dataset.created is None
    assert dataset.updated is None"""


############## InMemoryDatasetRepository #####################################################################################


def test_append_a_dataset_to_database():
    # Arrange
    dataset_dto = DataGouvDatasetDTO(buid="azerty", title="title", description="description")
    dataset = dataset_dto.convert_datagouv_dto_to_dataset()
    repository = InMemoryDatasetRepository(db=[])
    # Act
    repository.create_dataset(dataset)
    # Assert
    assert len(repository.db) == 1


def test_get_a_dataset_from_repository():
    # Arrange
    dataset_dto = DataGouvDatasetDTO(buid="azerty", title="title", description="description")
    dataset = dataset_dto.convert_datagouv_dto_to_dataset()
    repository = InMemoryDatasetRepository(db=[dataset])
    buid = "azerty"
    # Act
    result = repository.get_dataset_by_buid(buid)
    # Assert
    assert result == dataset


def test_get_dataset_with_wrong_id_from_repository_should_return_none():
    # Arrange
    dataset_dto = DataGouvDatasetDTO(buid="azerty", title="title", description="description")
    dataset = dataset_dto.convert_datagouv_dto_to_dataset()
    repository = InMemoryDatasetRepository(db=[dataset])
    wrong_buid = "wrong_buid"
    # Act
    result = repository.get_dataset_by_buid(wrong_buid)
    # Assert
    assert result is None


################### POSTGRESDATASETREPOSITORY ########################################################


def test_postgres_create_dataset_with_verification(db_fixture):
    # On utilise ici la fixture db_fixture définie dans conftest qui vient redéfinir une partie des
    # variables d'environnement afin d'initialiser la connexion à la base de données dans votre environnement de test et non de prod !
    # Arrange
    print("Database connection information before tests:")
    print(f"DB Name: {os.environ.get('DB_NAME')}")
    print(f"DB Host: {os.environ.get('DB_HOST')}")
    print(f"DB User: {os.environ.get('DB_USER')}")
    print(f"DB Port: {os.environ.get('DB_PORT')}")
    # Arrange
    dataset = Dataset(
        buid="buid",
        dataset_uid="azerty",
        dataset_id="123",
        title="Title",
        description="Description",
        publisher="Publisher",
        created="2024-01-01",
        updated="2024-01-02",
    )
    repository = PostgresDatasetRepository(db_fixture)

    # Act
    repository.create_dataset(dataset)

    # Assert
    result = repository.get_dataset_by_buid("buid")
    assert result is not None, "Dataset should be inserted into the database"
    assert result.buid == dataset.buid
    assert result.dataset_uid == dataset.dataset_uid
    assert result.dataset_id == dataset.dataset_id
    assert result.title == dataset.title
    assert result.description == dataset.description
    assert result.publisher == dataset.publisher
    assert result.created == dataset.created
    assert result.updated == dataset.updated


def test_fetch_and_store_datasets_in_database():
    # Step 1: Fetch data from data.economie API
    data_eco_datasets = DataEcoDatasetDTO.fetch_data_from_dataeco()

    # Step 2: Save raw data to a JSON file
    DataEcoDatasetDTO.save_data_from_dataeco_to_json("tests/fixtures/data_eco_raw.json", data_eco_datasets)

    # Step 3: Load data from the JSON file
    with open("tests/fixtures/data_eco_raw.json", "r") as file:
        data_eco_raw = json.load(file)

    # Step 4: Convert raw data to DTO objects
    data_eco_dtos = DataEcoDatasetDTO.retrieve_and_convert_data_to_dataeco_dto(data_eco_raw)

    # Step 5: Convert DTO objects to Dataset objects
    datasets = []
    for data in data_eco_dtos[:5]:  # Select the first 5 datasets
        dataset = Dataset(
            buid=data.buid,
            dataset_id=data.dataset_id,
            dataset_uid=data.dataset_uid,
            title=data.title,
            description=data.description,
            publisher=data.publisher,
            created=data.created,
            updated=data.updated
        )
        datasets.append(dataset)

    # Step 6: Store datasets in the database
    repository = PostgresDatasetRepository(db_fixture)
    for dataset in datasets:
        repository.create_dataset(dataset)

    # Step 7: Retrieve stored datasets from the database and check if they exist
    for dataset in datasets:
        retrieved_dataset = repository.get_dataset_by_buid(dataset.buid)
        assert retrieved_dataset is not None
        assert retrieved_dataset.buid == dataset.buid
        assert retrieved_dataset.dataset_id == dataset.dataset_id
        assert retrieved_dataset.title == dataset.title
        assert retrieved_dataset.description == dataset.description
        assert retrieved_dataset.publisher == dataset.publisher
        assert retrieved_dataset.created == dataset.created
        assert retrieved_dataset.updated == dataset.updated

    print("Datasets stored in the database and retrieved successfully.")