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
    if pd.notnull(date_fuseau_horaire):  # Vérification des valeurs nulles ou NaN
        date_object = parser.parse(str(date_fuseau_horaire))  # Conversion en chaîne de caractères pour les valeurs non-chaîne
        formatted_date = date_object.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date
    else:
        return None  # Gérer les valeurs nulles ou NaN dans les dates

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
                
                # Insérer des données dans la table Users
                query = "SELECT id_user FROM Users WHERE username = %s"
                cursor.execute(query, (row['user'],))
                existing_user = cursor.fetchone()

                if not existing_user:
                    # insérer utilisateur
                    query = "INSERT INTO Users (username) VALUES (%s)"
                    cursor.execute(query, (row['user'],))
                    conn.commit()  # Valider pour récupérer l'ID auto-incrémenté
                    id_user_auto = cursor.lastrowid  # Récupérer l'ID auto-incrémenté
                else:
                    id_user_auto = existing_user[0]

                # Insérer des données dans la table Organizations
                query = "SELECT id_organization FROM Organizations WHERE name = %s"
                cursor.execute(query, (row['organization'],))
                existing_organization = cursor.fetchone()

                if not existing_organization:
                    # insérer organisation
                    query = "INSERT INTO Organizations (name) VALUES (%s)"
                    cursor.execute(query, (row['organization'],))
                    conn.commit()
                    id_organization_auto = cursor.lastrowid
                else:
                    id_organization_auto = existing_organization[0]

                # Insérer des données dans la table Datasets
                query = "SELECT id_data FROM Datasets WHERE id_dataset = %s"
                cursor.execute(query, (row['id_dataset'],))
                existing_dataset = cursor.fetchone()

                if not existing_dataset:
                    # Insérer dataset
                    query = "INSERT INTO Datasets (id_dataset, title, description, url, created, last_update, slug, nb_discussions, nb_followers, nb_reuses, nb_views, id_organization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(query, (row["id_dataset"], row["title_dataset"], row["description_dataset"], row["url_dataset"], created_dataset_formatted, last_update_dataset_formatted, row["slug"], row["nb_discussions"], row["nb_followers"], row["nb_reuses"], row["nb_views"], id_organization_auto))
                    conn.commit()
                    id_data_auto = cursor.lastrowid
                else:
                    id_data_auto = existing_dataset[0]

                # Insérer des données dans la table Discussions
                query = "SELECT id_disc FROM Discussions WHERE id_discussion = %s"
                cursor.execute(query, (row['id_discussion'],))
                existing_discussion = cursor.fetchone()

                if not existing_discussion:
                    # Insérer discussion
                    query = "INSERT INTO Discussions (id_discussion, created, closed, title, id_data) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (row["id_discussion"], created_discussion_formatted, closed_discussion_formatted, row["title_discussion"], id_data_auto))
                    conn.commit()
                    id_disc_auto = cursor.lastrowid
                else:
                    id_disc_auto = existing_discussion[0]

                # Insérer des données dans la table Messages
                query = "INSERT INTO Messages (message, posted_on, id_disc, id_user) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (row["message"], discussion_posted_on_formatted, id_disc_auto, id_user_auto))
                conn.commit()

            except mysql.connector.Error as err:
                print(f"Erreur lors de l'insertion des données : {err}")
                if conn:
                    conn.rollback()  # Annuler la transaction en cas d'erreur

        print("Données CSV importées avec succès dans les tables !")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'importation des données CSV : {err}")
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
