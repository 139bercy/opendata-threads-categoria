# Script d'extraction des discussions
import requests
import pandas as pd
import logging
from datetime import datetime
import os

# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../../../logs/data_acquisition/extraction_discussions/'  # Le nom du dossier que vous avez créé

# Générer un nom de fichier de journal unique basé sur la date et l'heure
log_filename = datetime.now().strftime("%Y-%m-%d") + "_extract_discussions.log"

# Spécifier le chemin complet du fichier de journal
log_file_path = os.path.join(log_folder_path, log_filename)

# Configurer les paramètres de journalisation avec le chemin complet
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')


def fetch_discussion_data(url):
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
    discussions_url = "https://www.data.gouv.fr/api/1/discussions/"
    extracted_discussion_data = fetch_discussion_data(discussions_url)

    # Code de traitement et enregistrement
    extracted_data  = []
    for item in extracted_discussion_data:
        created_date = datetime.strptime(item['created'][:10], "%Y-%m-%d").strftime("%d/%m/%Y")
        closed_date = datetime.strptime(item['closed'][:10], "%Y-%m-%d").strftime("%d/%m/%Y") if item['closed'] else None
        user = item['user']
        full_name = user['first_name'] + ' ' + user['last_name']
        discussion_list = item['discussion']
        print(discussion_list)
        for discussion in discussion_list:
            extracted_data .append({
                'id_discussion': item['id'],
                'id_dataset': item['subject']['id'],
                'title_discussion': item['title'],
                'user': full_name,
                'message': discussion['content'],
                'created': created_date,
                'closed': closed_date
            })

    df = pd.DataFrame(extracted_data)
    
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

    # Créer un dataframe à partir des nouvelles données
    #grouped_df.to_csv('../../../data/raw/data_acquisition/extraction_discussions/discussions.csv', index=False)
    df.to_csv('../../../data/raw/data_acquisition/extraction_discussions/discussions.csv', index=False)
    logging.info("Les données ont été exportées avec succès vers 'discussions.csv'.")
    print("Les données ont été exportées avec succès vers 'discussions.csv'.")

if __name__ == "__main__":
    try:
        main()
    finally:
        # Fermez le fichier de journal
        logging.shutdown()
