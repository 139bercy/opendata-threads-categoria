from src.config import postgres_client
from src.core.gateways import AbstractThreadRepository, AbstractDatasetRepository
from src.core.models import Message, Thread, Dataset


class InMemoryDatasetRepository(AbstractDatasetRepository):
    def __init__(self, db):
        self.db = db

    def create_dataset(self, dataset: Dataset) -> None:
        dataset.pk = len(self.db) + 1
        self.db.append(dataset.__dict__)

    def get_dataset_by_buid(self, buid: str) -> Dataset:
        return next((Dataset(**data) for data in self.db if data["buid"] == buid), None)


class InMemoryThreadRepository(AbstractThreadRepository):
    def __init__(self, db):
        self.db = db

    def get_message_by_sk(self, sk: str) -> Message:
        return next((Message(**data) for data in self.db if data["sk"] == sk), None)

    def get_thread_by_sk(self, sk: str) -> Thread:
        return next((Thread(**data) for data in self.db if data["sk"] == sk), None)

    def create_message(self, message: Message) -> None:
        message.pk = len(self.db) + 1
        self.db.append(message.__dict__)

    def create_thread(self, thread: Thread) -> None:
        thread.pk = len(self.db) + 1
        self.db.append(thread.__dict__)


class PostgresThreadRepository(AbstractThreadRepository):
    # ADD_ONE ET FETCH_ONE SONT DÉFINIENT DANS LA CLASSE POSTGRESCLIENT (SRC/COMMON/INFRASTRUCTURE)
    def __init__(self, postgres_client):
        self.postgres_client = postgres_client

    def get_dataset_by_buid(self, buid) -> Dataset:
        query = f"SELECT * FROM dataset WHERE buid = %s;"
        result = postgres_client.fetch_one(query, (buid,))

        if result:
            # Construire l'objet Dataset à partir des données récupérées
            dataset = Dataset(
                buid=result["buid"],
                dataset_uid=result["dataset_uid"],
                dataset_id=result["dataset_id"],
                title=result["title"],
                description=result["description"],
                publisher=result["publisher"],
                created=result["created"],
                updated=result["updated"],
                # pk=result['pk'],
            )
            return dataset
        else:
            return None

    def get_message_by_sk(self, sk: str) -> Message:
        pass

    def get_thread_by_sk(self, sk: str) -> Thread:
        pass

    def create_message(self, message: Message) -> None:
        query = f"""INSERT INTO message(sk, thread_id, author, content, posted_on) VALUES ('{message.sk}', '{message.thread_id}','{message.author}', $${message.content}$$, '{message.posted_on}');"""
        postgres_client.add_one(query=query)

    def create_thread(self, thread: Thread) -> None:
        # query = f"""INSERT INTO thread(sk, title, created_on) VALUES ('{thread.sk}', '{thread.title}', '{thread.created_on}');"""
        # self.client.add_one(query=query)
        pass


class PostgresDatasetRepository(AbstractDatasetRepository):
    def __init__(self, postgres_client):
        self.postgres_client = postgres_client

    def create_dataset(self, dataset: Dataset) -> None:
        query = f"""
            INSERT INTO dataset(buid, dataset_uid, dataset_id, title, description, publisher, created, updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (dataset.buid, dataset.title, dataset.description)
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
