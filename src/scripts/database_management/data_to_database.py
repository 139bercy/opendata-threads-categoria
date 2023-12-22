import json
import logging
import os
import sys

import mysql.connector
import pandas as pd
from dateutil import parser

sys.path.append("..")
from logging_config import configure_logging


# Charger les informations de connexion depuis le fichier de configuration
with open("../../../config.json") as config_file:
    config = json.load(config_file)

# Utilisation des paramètres de connexion
db_host = config["DB_HOST"]
db_user = config["DB_USER"]
# db_password = config['DB_PASSWORD']
db_name = config["DB_NAME"]


def format_datetime_mysql(date_fuseau_horaire):
    if pd.notnull(date_fuseau_horaire):  # Vérification des valeurs nulles ou NaN
        date_object = parser.parse(
            str(date_fuseau_horaire)
        )  # Conversion en chaîne de caractères pour les valeurs non-chaîne
        formatted_date = date_object.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date
    else:
        return None  # Gérer les valeurs nulles ou NaN dans les dates


def import_data_from_csv():
    conn = None
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            # password= db_password,
            database="database_discussions",
        )

        if conn.is_connected():
            print("Connecté à la base de données MySQL")

    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        # Logging : Enregistrement d'une erreur de connexion
        logging.error(f"Erreur de connexion à la base de données: {e}")

    try:
        # Démarrer une transaction
        conn.start_transaction()

        # Charger les données CSV dans un DataFrame
        #if os.path.exists("../../../data/raw/data_acquisition/merging_data/dataset_mefsin.csv"):
        #    data = pd.read_csv("../../../data/raw/data_acquisition/merging_data/dataset_mefsin.csv")
        if os.path.exists("../../../data/raw/inference/predicted_data_models.csv"):
            data = pd.read_csv("../../../data/raw/inference/predicted_data_models.csv")
        else:
            raise Exception("Le fichier CSV n'existe pas...")

        # Créer un curseur
        cursor = conn.cursor()

        # Itérer sur les lignes du DataFrame et insérer les données dans les tables
        for index, row in data.iterrows():
            try:
                # Reformater les dates avec fuseau horaire en format DATETIME AAAA-MM-DD HH:MI:SS
                created_dataset_formatted = format_datetime_mysql(row["created_dataset"])
                #last_update_script_formatted = format_datetime_mysql(row["last_update_script"])
                discussion_posted_on_formatted = format_datetime_mysql(row["discussion_posted_on"])
                created_discussion_formatted = format_datetime_mysql(row["created_discussion"])
                closed_discussion_formatted = format_datetime_mysql(row["closed_discussion"])
                last_modified_dataset_formatted = format_datetime_mysql(row["last_modified_dataset"])

                # Insérer des données dans la table user
                # Vérifier si l'utilisateur avec le même prénom existe déjà
                query_check_user = "SELECT pk FROM user WHERE firstname = %s AND lastname = %s"
                cursor.execute(query_check_user, (row["firstname"], row["lastname"]))
                existing_user = cursor.fetchone()

                if not existing_user:
                    # Si l'utilisateur n'existe pas, l'insérer dans la table user
                    query_insert_user = "INSERT INTO user (firstname, lastname) VALUES (%s, %s)"
                    cursor.execute(query_insert_user, (row["firstname"], row["lastname"]))
                    conn.commit()  # Valider pour récupérer l'ID auto-incrémenté
                    id_user_auto = cursor.lastrowid  # Récupérer l'ID auto-incrémenté
                else:
                    # Si l'utilisateur existe déjà, récupérer son ID
                    id_user_auto = existing_user[0]

                # Insérer des données dans la table organization
                query = "SELECT pk FROM organization WHERE name = %s"
                cursor.execute(query, (row["organization"],))
                existing_organization = cursor.fetchone()

                if not existing_organization:
                    # insérer organisation
                    query = "INSERT INTO organization (name) VALUES (%s)"
                    cursor.execute(query, (row["organization"],))
                    conn.commit()
                    id_organization_auto = cursor.lastrowid
                else:
                    id_organization_auto = existing_organization[0]

                # Insérer des données dans la table dataset
                query = "SELECT pk FROM dataset WHERE dataset_buid = %s"
                cursor.execute(query, (row["id_dataset"],))
                existing_dataset = cursor.fetchone()

                if not existing_dataset:
                    # Insérer dataset
                    query = "INSERT INTO dataset (organization_id, dataset_buid, title, groupe_metier, description, url, created_at, last_modified_at, slug, nb_discussions, nb_followers, nb_reuses, nb_views) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(
                        query,
                        (
                            id_organization_auto,
                            row["id_dataset"],
                            row["title_dataset"],
                            row["groupe-metier"],
                            row["description_dataset"],
                            row["url_dataset"],
                            created_dataset_formatted,
                            last_modified_dataset_formatted,
                            row["slug"],
                            row["nb_discussions"],
                            row["nb_followers"],
                            row["nb_reuses"],
                            row["nb_views"],
                        ),
                    )
                    conn.commit()
                    id_dataset_auto = cursor.lastrowid
                else:
                    id_dataset_auto = existing_dataset[0]

                # Insérer des données dans la table discussion
                query = "SELECT pk FROM discussion WHERE discussion_buid = %s"
                cursor.execute(query, (row["id_discussion"],))
                existing_discussion = cursor.fetchone()

                if not existing_discussion:
                    # Insérer discussion
                    query = "INSERT INTO discussion (dataset_id, discussion_buid, created_at, closed_at, title) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(
                        query,
                        (
                            id_dataset_auto,
                            row["id_discussion"],
                            created_discussion_formatted,
                            closed_discussion_formatted,
                            row["title_discussion"],
                        ),
                    )
                    conn.commit()
                    id_discussion_auto = cursor.lastrowid
                else:
                    id_discussion_auto = existing_discussion[0]

                # Insérer des données dans la table message
                query = "INSERT INTO message (discussion_id, user_id, message, created_at, categorie, sous_categorie) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    query, (id_discussion_auto, id_user_auto, row["message"], discussion_posted_on_formatted, row["predictions_motifs_label"], row["predictions_ssmotifs_label"])
                )
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
    log_file_name = "data_to_database"
    configure_logging(log_directory, log_file_name)

    logging.info("Importation des données csv et remplissage des tables...")
    import_data_from_csv()
