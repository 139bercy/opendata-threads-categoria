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

    def import_datasets(self, data, repository):
        #for item in data:
        pass
    
                        
    """def import_discussions(self, data, repository):
        for item in data:
            for discussion in item["discussion"]:
                create_message(
                    repository = repository,
                    dataset_id = item["subject"]["id"],
                    thread_id = item["id"],
                    #author_slug = discussion["posted_by"]["slug"],
                    author = discussion["posted_by"]["first_name"] + ' ' + discussion["posted_by"]["last_name"],
                    content = discussion["content"],
                    posted_on = discussion["posted_on"],
                    #
                    created = item["created"],
                    closed = item["closed"],
                    title = item["title"],        
                )"""          
                
    def import_discussions(self, data, repository):
        for item in data:
            for discussion in item["discussion"]:
                print("Dataset ID:", item["subject"]["id"])
                print("Discussion_ID:", item["id"])
                print("Author:", discussion["posted_by"]["first_name"] + ' ' + discussion["posted_by"]["last_name"])
                print("Content:", discussion["content"])
                print("Message_Posted_On:", discussion["posted_on"])
                print("Discussion_Created_On:", item["created"])
                print("Discussion_Closed_On:", item["closed"])
                print("Title_Discussion:", item["title"])
                print("\n")

                """create_message(
                    repository=repository,
                    dataset_id=item["subject"]["id"],
                    discussion_id=item["id"],
                    author=discussion["posted_by"]["first_name"] + ' ' + discussion["posted_by"]["last_name"],
                    content=discussion["content"],
                    mesage_posted_on=discussion["posted_on"],
                    discussion_created=item["created"],
                    discussion_closed=item["closed"],
                    title=item["title"],
                )"""

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
