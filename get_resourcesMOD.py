import json
import requests

from src.core.infrastructure import PostgresThreadRepository
from src.core.usecases import create_message

        
class APIDataFetcher:
    def __init__(self, base_url, organization, data_folder="data"):
        self.base_url = base_url
        self.organization = organization
        self.data_folder = data_folder

    def fetch_data(self, resource):
        url = f"{self.base_url}/{self.organization}/{resource}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data for {resource}. Status code: {response.status_code}")
            return None

    def save_to_json(self, resource, data):
        filename = f"{self.data_folder}/{resource}.json" if resource != "catalog.json" else f"{self.data_folder}/{resource}"
        with open(filename, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Data for {resource} saved successfully.")

    def process_resource(self, resource, repository):
        data = self.fetch_data(resource)
        if data:
            self.save_to_json(resource, data)
            self.import_messages_from_json(resource, repository)

    def import_messages_from_json(self, resource, repository):
        filename = f"{self.data_folder}/{resource}.json" if resource != "catalog.json" else f"{self.data_folder}/{resource}"
        with open(filename, "r") as file:
            data = json.load(file)
            
            if resource == "datasets":
                self.import_datasets(data, repository)
            elif resource == "discussions":
                self.import_discussions(data, repository)
            elif resource == "catalog.json":
                self.import_catalog(data, repository)
            else:
                print(f"Unsupported resource: {resource}")

    # Import des données concernant le jeu de données en question
    def import_datasets(self, data, repository):
        # Initialisation d'un compteur
        dataset_count = 0
        # Itération à travers les éléments
        #for item in data["data"]:
        for dataset in data["data"]:
            # Accédez aux champs spécifiés
            print("title_dataset:", dataset["title"])
            print("description_dataset:", dataset["description"])
            print("organization:", dataset["organization"]["name"])
            print("url_dataset:", dataset["page"])
            print("nb_discussions:", dataset["metrics"]["discussions"])
            print("nb_followers:", dataset["metrics"]["followers"])
            print("nb_reuses:", dataset["metrics"]["reuses"])
            print("nb_views:", dataset["metrics"]["views"])
            print("remote_id_dataEco:", dataset["harvest"]["remote_id"] if dataset['harvest'] and 'remote_id' in dataset['harvest'] else None)
            print("slug_dataGouv:", dataset["slug"]) #slug sur data.gouv mais sur data.eco, l'équivalent est 'remote_id'
            print("created_dataset:", dataset["created_at"])
            #"last_update_dataset": dataset_updated_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            print('\n')
            dataset_count += 1
            
        # Imprimez le nombre total de données récupérées
        print(f"Total datasets recupérés: {dataset_count}")
            
    # Import des données concernant les discussions                     
    def import_discussions(self, data, repository):
        """for item in data:
            for discussion in item["discussion"]:
                print("Dataset_ID:", item["subject"]["id"])
                print("Discussion_ID:", item["id"])
                print("Author:", discussion["posted_by"]["first_name"] + ' ' + discussion["posted_by"]["last_name"])
                print("Content:", discussion["content"])
                print("Message_Posted_On:", discussion["posted_on"])
                print("Discussion_Created_On:", item["created"])
                print("Discussion_Closed_On:", item["closed"])
                print("Title_Discussion:", item["title"])
                print("\n")
                
                create_message(
                    repository=repository,
                    dataset_id=item["subject"]["id"],
                    discussion_id=item["id"],
                    #author_slug = discussion["posted_by"]["slug"],
                    author=discussion["posted_by"]["first_name"] + ' ' + discussion["posted_by"]["last_name"],
                    content=discussion["content"],
                    mesage_posted_on=discussion["posted_on"],
                    discussion_created=item["created"],
                    discussion_closed=item["closed"],
                    title=item["title"],
                )""" 
        pass

    def import_catalog(self, data, repository):
        pass


if __name__ == "__main__":
    
    base_url = "https://www.data.gouv.fr/api/1/organizations"
    organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
    resources = ["datasets", "discussions", "catalog.json"]

    repository = PostgresThreadRepository()
    data_fetcher = APIDataFetcher(base_url, organization)

    for resource in resources:
        data_fetcher.process_resource(resource, repository)
