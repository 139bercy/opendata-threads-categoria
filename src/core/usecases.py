from src.core.models import Message, Thread, Dataset
from src.core.gateways import AbstractThreadRepository, AbstractDatasetRepository


"""def create_dataset(
    repository: AbstractDatasetRepository, title: str, description: str
) -> Dataset:
    dataset = Dataset.create_dataset(title=title, description=description)
    repository.create_dataset(dataset)
    return dataset
"""


def create_dataset(repository: AbstractDatasetRepository, dataset: Dataset) -> Dataset:
    """
    Crée un jeu de données à partir des données provenant de DataGouv.
    """
    dataset = Dataset.create_dataset(
        dataset_uid=dataset.dataset_uid,
        dataset_id=dataset.dataset_id,
        title=dataset.title,
        description=dataset.description,
        publisher=dataset.publisher,
        created=dataset.created,
        updated=dataset.updated,  # ,
        # published=dataset.published,
        # restricted=dataset.restricted
    )
    repository.create_dataset(dataset)
    return dataset


def create_message(
    repository: AbstractThreadRepository, thread_id: str, author: str, content: str, posted_on: str
) -> Message:
    message = Message.create_message(thread_id=thread_id, author=author, content=content, posted_on=posted_on)
    repository.create_message(message)
    return message


def create_thread(repository: AbstractThreadRepository, title: str) -> Thread:
    thread = Thread.create_thread(title=title)
    repository.create_thread(thread)
    return thread
