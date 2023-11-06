import os
import requests
import pandas as pd
import logging
from datetime import datetime, timezone
import time

import sys
sys.path.append('..')
from logging_config import configure_logging

"""# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../../../logs/data_acquisition/extraction_discussions/'  # Le nom du dossier que vous avez créé

# Générer un nom de fichier de journal unique basé sur la date et l'heure
log_filename = datetime.now().strftime("%Y-%m-%d") + "_extract_discussions.log"

# Spécifier le chemin complet du fichier de journal
log_file_path = os.path.join(log_folder_path, log_filename)

# Configurer les paramètres de journalisation avec le chemin complet
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')
"""

def fetch_discussion_data(url, last_update_date, max_retries=3):
    data_list = []
    page = 1
    retries = 0
    
    while url and retries < max_retries:
        try:
            response = requests.get(url)
            response_json = response.json()
        except ValueError:
            logging.error("Erreur de décodage JSON. Ignorer cette page.")
            continue

        if response.ok:
            data = response_json["data"]

            # Filtrer les données pour ne récupérer que celles après la date de dernière mise à jour
            filtered_data = [item for item in data if parse_datetime(item['created']) >= last_update_date]

            data_list.extend(filtered_data)

            next_page = response_json["next_page"]
            url = next_page if next_page else None

            logging.info(f"Page {page} traitée !")
            page += 1
        else:
            logging.error(f"Request error: {response.status_code}. Retrying...")
            retries += 1
            time.sleep(5)  # Attendre quelques secondes avant de réessayer

    if retries == max_retries:
        logging.error("Maximum retries reached. Could not fetch data.")

    return data_list

def parse_datetime(datetime_str):
    return datetime.fromisoformat(datetime_str)

def load_existing_data(file_path):
    if os.path.exists(file_path):
        # Lire les données CSV en spécifiant le type des colonnes de dates
        date_columns = ['created_discussion', 'closed_discussion']
        return pd.read_csv(file_path, parse_dates=date_columns)
    else:
        return pd.DataFrame()

def save_extracted_data(data, file_path):
    data.to_csv(file_path, index=False)

def main():
    discussions_url = "https://www.data.gouv.fr/api/1/discussions/"
    existing_data_path = '../../../data/raw/data_acquisition/extraction_discussions/discussions.csv'
    
    if os.path.exists(existing_data_path):
        # Si le fichier CSV existe, chargez les données existantes
        existing_data = load_existing_data(existing_data_path)
        # Obtenez la date de dernière mise à jour à partir du fichier CSV existant
        last_update_date_str = existing_data['discussion_posted_on'].max()
        # Convertissez la date en objet datetime conscient du fuseau horaire UTC
        last_update_date = parse_datetime(last_update_date_str).replace(tzinfo=timezone.utc)
    else:
        # Si le fichier CSV n'existe pas, utilisez une date de départ arbitraire (par exemple, la date minimale)
        last_update_date = datetime.min.replace(tzinfo=timezone.utc)
        existing_data = pd.DataFrame()

    new_discussion_data = fetch_discussion_data(discussions_url, last_update_date)

    if new_discussion_data:
        # Extraction et traitement des nouvelles données
        extracted_data = []
        for item in new_discussion_data:
            #created_date = datetime.strptime(item['created'][:10], "%Y-%m-%d").strftime("%d/%m/%Y")
            #closed_date = datetime.strptime(item['closed'][:10], "%Y-%m-%d").strftime("%d/%m/%Y") if item['closed'] else None
            user = item['user']
            full_name = user['first_name'] + ' ' + user['last_name']
            discussion_list = item['discussion']
            for discussion in discussion_list:
                extracted_data.append({
                    'id_discussion': item['id'],
                    'id_dataset': item['subject']['id'],
                    'title_discussion': item['title'],
                    'user': full_name,
                    'message': discussion['content'],
                    #'created_discussion': created_date,
                    'created_discussion': discussion['created_discussion'],
                    #'closed_discussion': closed_date,
                    'closed_discussion': discussion['closed_discussion'],
                    'discussion_posted_on': discussion['posted_on']
                })
                
        ################################################################################################
        ################################################################################################
        ################################################################################################
        # Regrouper les discussions ayant le même id_discussion
        #grouped_df = df.groupby('id_discussion').agg({
        #    'id_dataset': 'first',
        #    'title_discussion': 'first',
        #    'user': 'first',
        #    'message': ' '.join,  # Groupement par message
        #    'created': 'first',
        #    'closed': 'first'
        #}).reset_index()
        
        # Utiliser value_counts pour compter le nombre de messages pour chaque id_discussion
        #message_counts = df['id_discussion'].value_counts()

        # Ajouter une colonne pour le nombre de messages dans grouped_df
        #grouped_df['message_count'] = grouped_df['id_discussion'].map(message_counts)
        ################################################################################################
        ################################################################################################
        ################################################################################################

        if extracted_data:
            # Fusionnez les nouvelles données avec les données existantes
            new_data = pd.DataFrame(extracted_data)
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
            
            # Enregistrez l'ensemble complet de données dans le fichier CSV
            save_extracted_data(combined_data, existing_data_path)
            print("Les nouvelles données ont été ajoutées au fichier CSV existant avec succès.")
        else:
            print("Aucune nouvelle donnée n'a été trouvée.")
    else:
        print("Aucune nouvelle donnée n'a été trouvée.")

if __name__ == "__main__":
    try:
        # Utilisation de la fonction pour configurer le logging
        log_directory = '../../../logs/data_acquisition/extraction_discussions/'
        log_file_name = 'extract_discussions'
        configure_logging(log_directory, log_file_name)

        main()
        logging.info("Les données ont été exportées avec succès vers 'discussions.csv'.")
        print("Les données ont été exportées avec succès vers 'discussions.csv'.")
    finally:
        # Fermez le fichier de journal
        logging.shutdown()
        
        
