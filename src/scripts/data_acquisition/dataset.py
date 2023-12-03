import requests
import pandas as pd
import logging
from datetime import datetime
import os
import pytz
import json

import sys

sys.path.append("..")
from logging_config import configure_logging


# Chargement des données existantes depuis un fichier CSV
def load_existing_data(file_path):
    if os.path.exists(file_path):
        try:
            existing_data_frame = pd.read_csv(file_path)
            return existing_data_frame
        except FileNotFoundError as e:
            logging.error(f"Fichier CSV non trouvé. Erreur : {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du fichier CSV. Erreur : {e}")
            sys.exit(1)
    else:
        return None  # Retourne None si le fichier n'existe pas


# Récupération des données depuis l'URL en filtrant par date et traitement direct
def fetch_and_process_data(url, last_update_script):
    extracted_data = []  # Initialisation de la liste
    page = 1
    while url:
        try:
            logging.info(f"Starting new HTTPS connection... ({page}): {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
            response_json = response.json()
            logging.debug(f"Response JSON for page {page}: {response_json}")
        except json.JSONDecodeError as json_err:
            logging.error(f"Error decoding JSON response ({page}): {json_err}")
            logging.debug(f"Error occurred at page {page}. Response JSON snippet: {json_err.doc}")
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error ({page}): {errh}")
            sys.exit(1)
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Error Connecting ({page}): {errc}")
            sys.exit(1)
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error ({page}): {errt}")
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            logging.error(f"Something went wrong ({page}): {err}")
            sys.exit(1)

        if "data" in response_json:
            data = response_json["data"]
            for item in data:
                last_modified_dataset = item.get("last_modified_dataset", None)
                if last_modified_dataset is None or (
                    last_modified_dataset and last_modified_dataset >= last_update_script
                ):
                    organization = item["organization"]["name"] if item["organization"] else None
                    metrics_discussions = (
                        item["metrics"]["discussions"]
                        if "metrics" in item and "discussions" in item["metrics"]
                        else None
                    )
                    metrics_followers = (
                        item["metrics"]["followers"] if "metrics" in item and "followers" in item["metrics"] else None
                    )
                    metrics_reuses = (
                        item["metrics"]["reuses"] if "metrics" in item and "reuses" in item["metrics"] else None
                    )
                    metrics_views = (
                        item["metrics"]["views"] if "metrics" in item and "views" in item["metrics"] else None
                    )

                    extracted_data.append(
                        {
                            "id_dataset": item["id"],
                            "title_dataset": item["title"],
                            "description_dataset": item["description"],
                            "organization": organization,
                            "url_dataset": item["page"],
                            "nb_discussions": metrics_discussions,
                            "nb_followers": metrics_followers,
                            "nb_reuses": metrics_reuses,
                            "nb_views": metrics_views,
                            "slug": item["slug"],
                            "created_dataset": item["created_at"],
                            "last_modified_dataset": item["last_modified"],
                            "last_update_script": datetime.now(),
                        }
                    )

            # Ajoutez cette ligne pour imprimer le nombre d'éléments extraits
            logging.info(f"Nombre d'éléments extraits jusqu'à la page {page}: {len(extracted_data)}")

            next_page = response_json.get("next_page")
            url = next_page if next_page else None

            logging.info(f"Page {page} traitée !")
            logging.debug(f"Response for page {page}: {response.status_code} - {url}")
            page += 1
        else:
            logging.error(f"Response does not contain 'data' key ({page}): {response.status_code} - URL : {url}")
            sys.exit(1)

    return pd.DataFrame(extracted_data)


# Enregistrement des données dans un fichier CSV
def save_data_to_csv(data_frame, file_path):
    try:
        data_frame.to_csv(file_path, index=False)
        logging.info("Les nouvelles données ont été fusionnées avec succès !")
        print("Les nouvelles données ont été fusionnées avec succès !")
    except Exception as e:
        logging.error(f"Erreur lors de l'enregistrement des données : {e}")
        print(f"Erreur lors de l'enregistrement des données : {e}")


def main():
    # Utilisation de la fonction pour configurer le logging
    log_directory = "../../../logs/data_acquisition/extraction_datasets/"
    log_file_name = "extract_datasets"
    configure_logging(log_directory, log_file_name)

    datasets_url = "https://www.data.gouv.fr/api/1/datasets/"
    existing_data_path = "../../../data/raw/data_acquisition/extraction_datasets/datasets.csv"

    # Chargement des données existantes
    existing_data_frame = load_existing_data(existing_data_path)

    if existing_data_frame is None:
        # Si le DataFrame existant est None, toutes les données sont utilisées
        last_update_script = datetime.min.replace(tzinfo=pytz.UTC)
    else:
        # Sinon, utilisez la date maximale du DataFrame existant
        last_update_script = (
            existing_data_frame["last_update_script"].max()
            if "last_update_script" in existing_data_frame.columns
            else datetime.min.replace(tzinfo=pytz.UTC)
        )

    # Récupération des nouvelles données depuis l'API en filtrant par date et traitement direct
    df = fetch_and_process_data(datasets_url, last_update_script)

    # Ajouter les nouvelles données filtrées au DataFrame existant
    existing_data_frame = pd.concat([existing_data_frame, df], ignore_index=True)

    # Enregistrement des données dans un fichier CSV
    save_data_to_csv(existing_data_frame, existing_data_path)


if __name__ == "__main__":
    try:
        main()
    finally:
        # Fermeture du fichier de journal
        logging.shutdown()
