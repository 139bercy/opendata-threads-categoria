import mysql.connector
import pandas as pd
import logging
import os
import json
from dateutil import parser

import sys
sys.path.append('..')
from logging_config import configure_logging

"""# Configuration du logging
log_directory = "../../../logs/database_management/"
log_file = os.path.join(log_directory, 'data_to_database.log')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
"""

# Charger les informations de connexion depuis le fichier de configuration
with open('../../../config.json') as config_file:
    config = json.load(config_file)

# Utilisation des paramètres de connexion
db_host = config['DB_HOST']
db_user = config['DB_USER']
#db_password = config['DB_PASSWORD']
db_name = config['DB_NAME']

def format_datetime_mysql(date_fuseau_horaire):
    # Convertir la chaîne de date en objet datetime
    date_object = parser.parse(date_fuseau_horaire)
    # Reformater la date
    formatted_date = date_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

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
                # Reformater les dates avec fuseau horaire en format DATETIME AAAA-MM-DD HH:MI:SS
                created_dataset_formatted = format_datetime_mysql(row["created_dataset"])
                last_update_dataset_formatted = format_datetime_mysql(row["last_update_dataset"])
                discussion_posted_on_formatted = format_datetime_mysql(row["discussion_posted_on"])
                created_discussion_formatted = format_datetime_mysql(row["created_discussion"])
                closed_discussion_formatted = format_datetime_mysql(row["closed_discussion"])

                # Insérer des données dans la table User
                #query = "INSERT INTO nom_Table (colonne1, colonne2, colonne3) VALUES (%s, %s, %s)" 
                query = "INSERT INTO  User (username) VALUES (%s)" 
                # Exécution de la requête d'insertion pour chaque ligne du DataFrame
                #cursor.execute(query, (row['colonne1'], row['colonne2'], row['colonne3']))  # Remplacer avec les noms des colonnes du dataframe csv
                cursor.execute(query, (row['user'],))
                
                # Récupérer l'ID auto-incrémenté de la dernière opération d'insertion
                id_user_auto = cursor.lastrowid

                # Insérer des données dans la table Organization
                query = "INSERT INTO Organization (organization) VALUES (%s)"
                # Exécution de la requête d'insertion pour chaque ligne du DataFrame
                cursor.execute(query, (row['organization'],))
                
                # Récupérer l'ID auto-incrémenté de la dernière opération d'insertion
                id_organization_auto = cursor.lastrowid
                
                # Insérer des données dans la table Dataset
                query = "INSERT INTO Dataset (id_dataset, title_dataset, description_dataset, url_dataset, created_dataset, last_update_dataset, slug, nb_discussions, nb_followers, nb_reuses, nb_views, id_organization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                # Exécution de la requête d'insertion pour chaque ligne du DataFrame
                cursor.execute(query, (row["id_dataset"], row["title_dataset"], row["description_dataset"], row["url_dataset"], created_dataset_formatted, last_update_dataset_formatted, row["slug"], row["nb_discussions"], row["nb_followers"], row["nb_reuses"], row["nb_views"], id_organization_auto))
                
                # Récupérer l'ID auto-incrémenté de la dernière opération d'insertion
                id_dataset_auto = cursor.lastrowid
                
                # Insérer des données dans la table Discussion
                query = "INSERT INTO Discussion (id_discussion, created_discussion, closed_discussion, discussion_posted_on, title_discussion, message, id_user, id_dataset) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                # Exécution de la requête d'insertion pour chaque ligne du DataFrame
                cursor.execute(query, (row["id_discussion"], created_discussion_formatted, closed_discussion_formatted, discussion_posted_on_formatted, row["title_discussion"], row["message"], id_user_auto, id_dataset_auto))
            
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
    # Utilisation de la fonction pour configurer le logging
    log_directory = "../../../logs/database_management/data_to_database/"
    log_file_name = 'data_to_database'
    configure_logging(log_directory, log_file_name)

    logging.info("Importation des données csv et remplissage des tables...")
    import_data_from_csv()
