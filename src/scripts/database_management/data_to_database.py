import mysql.connector
import pandas as pd
import logging
import os
import json
from datetime import datetime
from dateutil import parser

# Configuration du logging
log_directory = "../../../logs/database_management/"
log_file = os.path.join(log_directory, 'data_to_database.log')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Charger les informations de connexion depuis le fichier de configuration
with open('../../../config.json') as config_file:
    config = json.load(config_file)

# Utilisation des paramètres de connexion
db_host = config['DB_HOST']
db_user = config['DB_USER']
#db_password = config['DB_PASSWORD']
db_name = config['DB_NAME']

def import_data_from_csv():
    conn = None
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host= db_host,
            user= db_user,
            #password= db_password,
            database="database_discussions"
        )
        
        if conn.is_connected():
            print('Connecté à la base de données MySQL')
        
    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        # Logging : Enregistrement d'une erreur de connexion
        logging.error(f"Erreur de connexion à la base de données: {e}")

    try:
        # Démarrer une transaction
        conn.start_transaction()
        
        # Charger les données CSV dans un DataFrame
        if os.path.exists("../../../data/raw/data_acquisition/merging_data/dataset_mefsin.csv"):
            data = pd.read_csv("../../../data/raw/data_acquisition/merging_data/dataset_mefsin.csv")
        else:
            raise Exception("Le fichier CSV n'existe pas...")
        
        # Créer un curseur
        cursor = conn.cursor()

        # Itérer sur les lignes du DataFrame et insérer les données dans la table Utilisateur
        for index, row in data.iterrows():
            try:
                # Insérer des données dans la table Utilisateur
                cursor.execute("""
                INSERT INTO Utilisateur (id_user, user)
                VALUES (%s)
                """, (row["user"],))
                
                # Insérer des données dans la table Organization
                cursor.execute("""
                INSERT INTO Organization (id_organization, organization)
                VALUES (%s)
                """, (row["organization"],))
                
                """# Supprimer la partie du fuseau horaire et convertir la date
                original_date = '2023-09-13T09:04:58.310000+0000'
                date_without_timezone = original_date.split('+')[0]  # Supprime le fuseau horaire
                formatted_last_update_date = datetime.strptime(date_without_timezone, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')"""

                # Insérer des données dans la table Dataset
                cursor.execute("""
                INSERT INTO Dataset (id_dataset, title_dataset, description_dataset, url_dataset, created_dataset, last_update_dataset, slug, nb_discussions, nb_followers, nb_reuses, nb_views, organization_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (row["title_dataset"], row["description_dataset"], row["url_dataset"], row["created_dataset"], row["last_update_dataset"], row["slug"], row["nb_discussions"], row["nb_followers"], row["nb_reuses"], row["nb_views"], row["organization"]))

                # Insérer des données dans la table Discussion
                cursor.execute("""
                INSERT INTO Discussion (id_discussion, created_discussion, closed_discussion, discussion_posted_on, title_discussion, message, user_id, id_dataset)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (row["created_discussion"], row["closed_discussion"], row["discussion_posted_on"], row["title_discussion"], row["message"], row["user"], row["id_dataset"]))
            
            except mysql.connector.Error as err:
                print(f"Erreur lors de l'insertion des données : {err}")
                # Logging : Enregistrement d'une erreur d'insertion
                logging.error(f"Erreur lors de l'insertion des données : {err}")
                if conn:
                    conn.rollback()  # Annuler la transaction en cas d'erreur

        # Valider les changements
        conn.commit()

        print("Données CSV importées avec succès dans les tables !")
        # Logging : Enregistrement d'un message de succès
        logging.info("Données CSV importées avec succès dans les tables !")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'importation des données CSV : {err}")
        # Logging : Enregistrement d'une erreur
        logging.error(f"Erreur lors de l'importation des données CSV : {err}")
        if conn:
            conn.rollback()  # Annuler la transaction en cas d'erreur

    finally:
        if conn:
            conn.close()  # Fermeture de la connexion

if __name__ == "__main__":
    logging.info("Importation des données csv et remplissage des tables...")
    import_data_from_csv()
