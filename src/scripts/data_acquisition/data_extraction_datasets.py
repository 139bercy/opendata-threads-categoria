# Script d'extraction des jeux de données 
import requests
import pandas as pd
import logging
from datetime import datetime
import os

# Spécifier le chemin relatif vers le dossier logs
##log_folder_path = '../logs'  # Le nom du dossier que vous avez créé

# Spécifier le chemin complet du fichier de journal
##log_file_path = f'{log_folder_path}/extract_datasets.log'

# Configurer les paramètres de journalisation
##logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(levelname)s: %(message)s')
#logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../logs/extract_datasets'  # Le nom du dossier que vous avez créé

# Générer un nom de fichier de journal unique basé sur la date et l'heure
log_filename = datetime.now().strftime("%Y-%m-%d") + "_extract_datasets.log"

# Spécifier le chemin complet du fichier de journal
log_file_path = os.path.join(log_folder_path, log_filename)

# Configurer les paramètres de journalisation avec le chemin complet
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

def fetch_dataset_data(url):
    data_list = []
    page = 1
    while url:
        try:
            response = requests.get(url)
            response_json = response.json()
        except ValueError:
            #print("Erreur de décodage JSON. Ignorer cette page.")
            logging.error("Erreur de décodage JSON. Ignorer cette page.")
            continue

        if response.ok:
            data = response_json["data"]
            data_list.extend(data)

            next_page = response_json["next_page"]
            url = next_page if next_page else None

            #print(f"Page {page} traitée !")
            logging.info(f"Page {page} traitée !")
            page += 1
        else:
            #print(f"Request error: {response.status_code}.")
            logging.error(f"Request error: {response.status_code}.")
            #print(response.text)
            break

    return data_list

def main():
    datasets_url = "https://www.data.gouv.fr/api/1/datasets/"
    extracted_dataset_data = fetch_dataset_data(datasets_url)

    # Code de traitement et enregistrement
    extracted_data = []
    for item in extracted_dataset_data:
        organization = item['organization']['name'] if item['organization'] else None
        metrics_discussions = item['metrics']['discussions'] if item['metrics'] else None
        metrics_followers = item['metrics']['followers'] if item['metrics'] else None
        metrics_reuses = item['metrics']['reuses'] if item['metrics'] else None
        metrics_views = item['metrics']['views'] if item['metrics'] else None
        extracted_data.append({
            'id_dataset': item['id'],
            'title_dataset': item['title'],
            'description_dataset': item['description'],
            'organization': organization,
            'url_dataset': item['page'],
            'nb_discussions': metrics_discussions,
            'nb_followers': metrics_followers,
            'nb_reuses': metrics_reuses,
            'nb_views': metrics_views,
        })

    df = pd.DataFrame(extracted_data)

    # Créer un dataframe à partir des nouvelles données
    df.to_csv('../data/raw/extraction/datasets.csv', index=False)
    #print("Les données ont été exportées avec succès vers 'datasets.csv'.")
    logging.info("Les données ont été exportées avec succès vers 'datasets.csv'.")
    print("Les données ont été exportées avec succès vers 'datasets.csv'.")


if __name__ == "__main__":
    try:
        main()
    finally:
        # Fermez le fichier de journal
        logging.shutdown()
        