from __future__ import annotations
from src.common.utils import sha256_hash_string

class Dataset:
    def __init__(self, buid: str, dataset_uid: str, dataset_id: str, title:str, description: str, publisher: str, created: str, updated: str,  pk: int=None) -> None:
        #self.pk = pk #Dataset_id fourni par les sources des données (DataGouv et DataEco) 
        self.buid = buid  #id généré par nous même (hash grâce à get_key() définie en dessous)
        self.dataset_uid = dataset_uid
        self.dataset_id = dataset_id
        self.title = title
        self.description = description
        self.publisher = publisher
        self.created = created
        self.updated = updated    
        #self.published = published
        #self.restricted = restricted

    @classmethod
    def create_dataset(cls, dataset_uid:str, dataset_id: str, title: str, description: str, publisher: str, created: str, updated: str) -> Dataset:
        """
        Crée une instance de Dataset avec une buid calculée à partir d'un hash du slug.
        """
        buid = get_key(f"{title}")   # VOIR pour remplacer buid par f"{slug}"", trouver une id_unique pour le dataset
        instance = cls(buid=buid, dataset_uid=dataset_uid, dataset_id=dataset_id, title=title, description=description, publisher=publisher, created=created, updated=updated)
        return instance
    

class Message:
    def __init__(self, sk: str, thread_id: str, author: str, content: str, posted_on: str, pk: int = None) -> None:
        self.pk = pk
        self.thread_id = thread_id
        self.posted_on = posted_on
        self.author = author
        self.content = content
        self.sk = sk  #buid (surogate key) hash

    @classmethod
    def create_message(cls, thread_id: str, author: str, content: str, posted_on: str) -> Message:
        """
        L'identifiant unique d'un message est un hash de la date de publication et du corps du message lui-même.
        Lié à une contrainte d'unicité en base de données, il permet de dédoublonner les ressources à l'import
        en tirant parti des fonctionnalités de la base de donnée.
        """
        sk = get_key(f"{posted_on}-{content}")
        instance = cls(sk=sk, thread_id=thread_id, author=author, content=content, posted_on=posted_on)
        return instance


class Thread:
    def __init__(self, sk: str, title: str, pk: int = None) -> None:
        self.pk = pk
        self.sk = sk
        self.title = title

    @classmethod
    def create_thread(cls, title: str) -> Thread:
        """
        TODO: La clef devrait être une combinaison de la date d'ouverture de la discussion et de son titre.
        """
        sk = get_key(f"{title}")
        instance = cls(sk=sk, title=title)
        return instance


def get_key(chain):
    """
    Utiliser les 8 premiers caractères d'un hash est à ce stade suffisamment discriminant pour éviter les collisions.
    """
    return sha256_hash_string(chain)[0:8]
