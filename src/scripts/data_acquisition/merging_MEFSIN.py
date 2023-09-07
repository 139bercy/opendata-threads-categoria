import pandas as pd
import logging
from datetime import datetime
import os

# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../logs/merging'  # Le nom du dossier que vous avez créé
# Générer un nom de fichier de journal unique basé sur la date et l'heure
log_filename = datetime.now().strftime("%Y-%m-%d") + "_merging.log"
# Spécifier le chemin complet du fichier de journal
log_file_path = os.path.join(log_folder_path, log_filename)
# Configurer les paramètres de journalisation avec le chemin complet
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Obtenez le chemin du dossier du script en cours d'exécution
script_directory = os.path.dirname(__file__)
# Chemin du dossier contenant les fichiers CSV relativement au script
csv_folder_path = os.path.join(script_directory, '../data/raw/')

def load_and_merge_data():
    try:
        # Charger les fichiers CSV
        logging.info("Chargement des fichiers CSV en cours...")
        df_discussions = pd.read_csv(os.path.join(csv_folder_path, 'discussions.csv'))
        df_datasets = pd.read_csv(os.path.join(csv_folder_path, 'datasets.csv'))
        logging.info("Fichiers CSV chargés avec succès.")

        # Fusionner les DataFrames en utilisant les colonnes 'id_subject' et 'id_dataset' comme clés de jointure
        logging.info("Fusion des DataFrames en cours...")
        df_merged = pd.merge(df_discussions, df_datasets, left_on='id_dataset', right_on='id_dataset', how='inner')
        logging.info("Fusion des DataFrames terminée.")
        
        # Enregistrer le DataFrame fusionné dans un fichier CSV
        merged_csv_path = os.path.join(csv_folder_path, 'merging/merged_data.csv')
        df_merged.to_csv(merged_csv_path, index=False)
        logging.info("Données fusionnées exportées avec succès au fichier merged_data.csv.")

        return df_merged
    
    except Exception as e:
        logging.error("Erreur lors du chargement et de la fusion des données : %s", str(e))
        return None
    

def filter_and_export_data(df_merged):
    # Filtrer le DataFrame MEFSIN en fonction de la colonne 'organization'
    try:
        logging.info("Filtrage des données en cours...")
        df_filtered = df_merged[df_merged['organization'] == "Ministère de l'Économie, des Finances et de la Souveraineté industrielle et numérique"]
        logging.info("Filtrage des données terminé.")

        # Export des données filtrées au format CSV
        csv_export_path = os.path.join(csv_folder_path, 'merging/dataset_MEFSIN.csv')
        df_filtered.to_csv(csv_export_path, index=False)
        logging.info("Données filtrées exportées avec succès au fichier dataset_MEFSIN.csv.")
    
    except Exception as e:
        logging.error("Erreur lors du filtrage et de l'export des données : %s", str(e))
        

if __name__ == "__main__":
    # Chargement et fusion des données
    df_merged = load_and_merge_data()

    if df_merged is not None:
        # Filtrage et export des données
        filter_and_export_data(df_merged)
        
    else:
        logging.error("Impossible de continuer sans données valides.")
        
    # Fermez le système de journalisation
    logging.shutdown()
    