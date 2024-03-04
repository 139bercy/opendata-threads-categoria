import json
import requests
import psycopg2

from src.core.infrastructure import PostgresThreadRepository

class APIDataFetcher:
    def __init__(self, api_sources, data_folder="data"):
        self.api_sources = api_sources
        self.data_folder = data_folder 

    def fetch_data_from_api(self, api_url):
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

    def save_data_to_json(self, resource, data):
        filename = f"{self.data_folder}/{resource}.json"
        with open(filename, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Data for {resource} saved successfully.")

    def load_db_config(self):
        with open("config.json") as config_file:
            return json.load(config_file)
        
    def insert_data_into_db(self, data):
        config = self.load_db_config()
        connection = None
        try:
            connection = psycopg2.connect(
                dbname=config["DB_NAME"],
                user=config["DB_USER"],
                password=config["DB_PASSWORD"],
                host=config["DB_HOST"]
            )
            cursor = connection.cursor()

            #Insertion des données en base
            #insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
            #cursor.execute(insert_query, (data_column1, data_column2))
            
            connection.commit()
            print("Data inserted into the database successfully")

        except Exception as e:
            print(f"Error inserting data into DB: {e}")

        finally:
            if connection is not None:
                cursor.close()
                connection.close()

    def fetch_and_process_data(self):
       for source in self.api_sources:
            data = self.fetch_data_from_api(source['url'])
            if data:
                self.save_data_to_json(resource, data)
                self.insert_data_into_db(data)


# Exemple d'utilisation
api_sources = [
    {"url": "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"},
    #{"url": "https://data.economie.gouv.fr/api/automation/v1.0/"}  # À compléter
]
resource = "datasetsV"
#resources = ["datasets", "discussions"]

data_fetcher = APIDataFetcher(api_sources)
data_fetcher.fetch_and_process_data()
