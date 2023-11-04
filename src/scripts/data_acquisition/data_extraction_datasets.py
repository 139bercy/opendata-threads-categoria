import requests
import pandas as pd
import logging
from datetime import datetime
import os
import pytz

import sys
sys.path.append('..')
from logging_config import configure_logging

"""# Configuration de la journalisation
def configure_logging(log_folder_path):
    log_filename = datetime.now().strftime("%Y-%m-%d") + "_extract_datasets.log"
    log_file_path = os.path.join(log_folder_path, log_filename)
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')"""

# Récupération des données depuis l'URL
def fetch_data_from_url(url):
    data_list = []
    page = 1
    while url:
        try:
            response = requests.get(url)
            response_json = response.json()
        except ValueError as e:
            logging.error(f"Erreur de décodage JSON. Ignorer cette page. Erreur : {e}")
            continue

        if response.ok:
            data = response_json.get("data", [])
            data_list.extend(data)

            next_page = response_json.get("next_page")
            url = next_page if next_page else None

            logging.info(f"Page {page} traitée !")
            page += 1
        else:
            logging.error(f"Request error: {response.status_code} - URL : {url}")
            break

    return data_list

# Chargement des données existantes depuis un fichier CSV
def load_existing_data(file_path):
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_csv(file_path)
            # Convertir la colonne 'last_update' en datetimes conscientes du fuseau horaire
            existing_data['last_update'] = pd.to_datetime(existing_data['last_update']).dt.tz_convert(pytz.UTC)
            return existing_data
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du fichier CSV. Erreur : {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def process_data(existing_data, extracted_dataset_data):
    extracted_data = []
    last_update_date = existing_data['last_update'].max() if not existing_data.empty else datetime.min.replace(tzinfo=pytz.UTC)

    for item in extracted_dataset_data:
        dataset_updated_date_str = item['last_update']
        
        # Check if milliseconds are present in the last_update field
        if "." in dataset_updated_date_str:
            # Handle milliseconds if present
            dataset_updated_date_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        else:
            # If no milliseconds, use a format without milliseconds
            dataset_updated_date_format = "%Y-%m-%dT%H:%M:%S%z"
        
        dataset_updated_date = datetime.strptime(dataset_updated_date_str, dataset_updated_date_format)
        dataset_updated_date = dataset_updated_date.replace(tzinfo=pytz.UTC)
        
        if dataset_updated_date >= last_update_date:
            organization = item['organization']['name'] if item['organization'] else None
            metrics_discussions = item['metrics']['discussions'] if item['metrics'] else None
            metrics_followers = item['metrics']['followers'] if item['metrics'] else None
            metrics_reuses = item['metrics']['reuses'] if item['metrics'] else None
            metrics_views = item['metrics']['views'] if item['metrics'] else None
            #remote_id = item['harvest']['remote_id'] if item['harvest'] and 'remote_id' in item['harvest'] else None
            
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
                #'remote_id': remote_id,
                'slug': item['slug'],
                'created_dataset': item['created_at'],
                'last_update_dataset': dataset_updated_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            })
            
    return pd.DataFrame(extracted_data)

# Enregistrement des données dans un fichier CSV
def save_data_to_csv(data, file_path):
    try:
        data.to_csv(file_path, index=False)
        logging.info("Les nouvelles données ont été fusionnées avec succès !")
        print("Les nouvelles données ont été fusionnées avec succès !")
    except Exception as e:
        logging.error(f"Erreur lors de l'enregistrement des données : {e}")
        print(f"Erreur lors de l'enregistrement des données : {e}")

def main():
    # Utilisation de la fonction pour configurer le logging
    log_directory = '../../../logs/data_acquisition/extraction_datasets/'
    log_file_name = 'extract_datasets'
    configure_logging(log_directory, log_file_name)

    datasets_url = "https://www.data.gouv.fr/api/1/datasets/"
    existing_data_path = '../../../data/raw/data_acquisition/extraction_datasets/datasets.csv'

    # Chargement des données existantes
    existing_data = load_existing_data(existing_data_path)

    # Récupération des nouvelles données
    extracted_dataset_data = fetch_data_from_url(datasets_url)

    # Traitement des données
    df = process_data(existing_data, extracted_dataset_data)

    # Fusionner les nouvelles données avec les données existantes
    combined_data = pd.concat([existing_data, df], ignore_index=True)

    # Enregistrement des données dans un fichier CSV
    save_data_to_csv(combined_data, existing_data_path)

if __name__ == "__main__":
    try:
        main()
    finally:
        # Fermeture du fichier de journal
        logging.shutdown()
