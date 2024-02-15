import json
import requests

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


if __name__ == "__main__":
    base_url = "https://www.data.gouv.fr/api/1/organizations"
    organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
    resources = ["datasets", "discussions", "catalog.json"]

    data_fetcher = APIDataFetcher(base_url, organization)

    for resource in resources:
        data = data_fetcher.fetch_data(resource)
        if data:
            data_fetcher.save_to_json(resource, data)
