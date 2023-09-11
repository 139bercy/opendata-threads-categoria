import requests
import pandas as pd
import logging
from datetime import datetime
import os

# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../../../logs/data_acquisition/extraction_datasets/'  # Le nom du dossier que vous avez créé

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
            logging.error("Erreur de décodage JSON. Ignorer cette page.")
            continue

        if response.ok:
            data = response_json["data"]
            data_list.extend(data)

            next_page = response_json["next_page"]
            url = next_page if next_page else None

            logging.info(f"Page {page} traitée !")
            page += 1
        else:
            logging.error(f"Request error: {response.status_code}.")
            break

    return data_list

def load_existing_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

def main():
    datasets_url = "https://www.data.gouv.fr/api/1/datasets/"
    existing_data_path = '../../../data/raw/data_acquisition/extraction_datasets/datasets.csv'

    # Obtenez la date de dernière modification du fichier CSV existant s'il existe
    if os.path.exists(existing_data_path):
        last_update_date = datetime.fromtimestamp(os.path.getmtime(existing_data_path))
    else:
        last_update_date = datetime.min  # Utilisez une date minimale si le fichier n'existe pas encore

    extracted_dataset_data = fetch_dataset_data(datasets_url)

    # Code de traitement et enregistrement
    extracted_data = []
    for item in extracted_dataset_data:
        # Comparez la date de dernière mise à jour avec la date du jeu de données
        dataset_updated_date = datetime.strptime(item['last_update'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if dataset_updated_date >= last_update_date:
            organization = item['organization']['name'] if item['organization'] else None
            metrics_discussions = item['metrics']['discussions'] if item['metrics'] else None
            metrics_followers = item['metrics']['followers'] if item['metrics'] else None
            metrics_reuses = item['metrics']['reuses'] if item['metrics'] else None
            metrics_views = item['metrics']['views'] if item['metrics'] else None
            remote_id = item['harvest']['remote_id'] if item['harvest'] and 'remote_id' in item['harvest'] else None
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
                'remote_id': remote_id,
            })

    df = pd.DataFrame(extracted_data)

    # Charger les données existantes
    existing_data = load_existing_data(existing_data_path)

    # Fusionner les nouvelles données avec les données existantes
    combined_data = pd.concat([existing_data, df], ignore_index=True)

    # Enregistrez les données fusionnées dans le fichier CSV
    combined_data.to_csv(existing_data_path, index=False)

    logging.info("Les nouvelles données ont été fusionnées avec succès avec les données existantes.")
    print("Les nouvelles données ont été fusionnées avec succès avec les données existantes.")


if __name__ == "__main__":
    try:
        main()
    finally:
        # Fermez le fichier de journal
        logging.shutdown()
