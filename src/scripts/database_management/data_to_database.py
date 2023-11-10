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
                
                # Insérer des données dans la table user
                #query = "SELECT pk FROM user WHERE username = %s"
                #cursor.execute(query, (row['user'],))
                #existing_user = cursor.fetchone()
                query = "SELECT pk FROM user WHERE CONCAT(firstname, ' ', lastname) = %s"
                cursor.execute(query, (row['firstname'] + ' ' + row['lastname'],))
                existing_user = cursor.fetchone()

                if not existing_user:
                    # insérer utilisateur
                    #query = "INSERT INTO user (username) VALUES (%s)"
                    #cursor.execute(query, (row['user'],))
                    query = "INSERT INTO Users (firstname, lastname) VALUES (%s, %s)"
                    cursor.execute(query, (row['firstname'], row['lastname'],))
                    conn.commit()  # Valider pour récupérer l'ID auto-incrémenté
                    id_user_auto = cursor.lastrowid  # Récupérer l'ID auto-incrémenté
                else:
                    id_user_auto = existing_user[0]

                # Insérer des données dans la table organization
                query = "SELECT pk FROM organization WHERE name = %s"
                cursor.execute(query, (row['organization'],))
                existing_organization = cursor.fetchone()

                if not existing_organization:
                    # insérer organisation
                    query = "INSERT INTO organization (name) VALUES (%s)"
                    cursor.execute(query, (row['organization'],))
                    conn.commit()
                    id_organization_auto = cursor.lastrowid
                else:
                    id_organization_auto = existing_organization[0]

                # Insérer des données dans la table dataset
                query = "SELECT pk FROM dataset WHERE dataset_buid = %s"
                cursor.execute(query, (row['id_dataset'],))
                existing_dataset = cursor.fetchone()

                if not existing_dataset:
                    # Insérer dataset
                    query = "INSERT INTO dataset (organization_id, dataset_buid, title, description, url, created_at, last_update, slug, groupe_metier, nb_discussions, nb_followers, nb_reuses, nb_views) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(query, (id_organization_auto, row["id_dataset"], row["title_dataset"], row["description_dataset"], row["url_dataset"], created_dataset_formatted, last_update_dataset_formatted, row["slug"], row["groupe_metier"], row["nb_discussions"], row["nb_followers"], row["nb_reuses"], row["nb_views"]))
                    conn.commit()
                    id_dataset_auto = cursor.lastrowid
                else:
                    id_dataset_auto = existing_dataset[0]

                # Insérer des données dans la table discussion
                query = "SELECT pk FROM discussion WHERE discussion_buid = %s"
                cursor.execute(query, (row['id_discussion'],))
                existing_discussion = cursor.fetchone()

                if not existing_discussion:
                    # Insérer discussion
                    query = "INSERT INTO discussion (dataset_id, discussion_buid, created_at, closed_at, title) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (id_dataset_auto, row["id_discussion"], created_discussion_formatted, closed_discussion_formatted, row["title_discussion"]))
                    conn.commit()
                    id_discussion_auto = cursor.lastrowid
                else:
                    id_discussion_auto = existing_discussion[0]

                # Insérer des données dans la table message
                query = "INSERT INTO message (discussion_id, user_id, message, created_at) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id_discussion_auto, id_user_auto, row["message"], discussion_posted_on_formatted))
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
