import json
import logging
import sys

import mysql.connector

sys.path.append("..")
from logging_config import configure_logging


# Récupérer le host, le nom d'utilisateur et le mot de passe à partir des variables d'environnement situées dans le fichier de conf.
def load_db_config():
    with open("../../../config.json") as config_file:
        return json.load(config_file)


def create_database_and_tables():
    config = load_db_config()

    db_host = config["DB_HOST"]
    db_user = config["DB_USER"]
    # db_password = config['DB_PASSWORD']
    # db_name = config['DB_NAME']

    try:
        # Connexion à MySQL avec les paramètres chargés depuis le fichier de configuration
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            # password=db_password
        )

        cursor = conn.cursor()

        # Création de la base de données
        cursor.execute("CREATE DATABASE IF NOT EXISTS database_discussions")

        # Utilisation de la base de données nouvellement créée
        cursor.execute("USE database_discussions")

        # Création de tables 
        # TABLE USER
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS user (
            pk INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL
        )
        """
        )

        # TABLE ORGANIZATION
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS organization (
            pk INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """
        )

        # TABLE DATASET
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS dataset (
            pk INT AUTO_INCREMENT PRIMARY KEY,
            dataset_buid VARCHAR(50) NOT NULL UNIQUE,
            title VARCHAR(400),
            groupe_metier VARCHAR(255),
            description TEXT,
            url VARCHAR(400),
            created_at DATETIME,
            last_modified_at DATETIME,
            slug VARCHAR(255) NOT NULL,
            nb_discussions INT,
            nb_followers INT,
            nb_reuses INT,
            nb_views INT,
            organization_id INT,
            FOREIGN KEY (organization_id) REFERENCES organization(pk)
        )
        """
        )

        # TABLE DISCUSSION
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS discussion (
            pk INT AUTO_INCREMENT PRIMARY KEY,
            discussion_buid VARCHAR(50) NOT NULL,
            created_at DATETIME,
            closed_at DATETIME,
            title VARCHAR(400),
            dataset_id INT,
            FOREIGN KEY (dataset_id) REFERENCES dataset(pk)
        )
        """
        )

        # TABLE MESSAGE
        # Table intermédiaire car relation (n,n)
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS message (
            pk INT AUTO_INCREMENT PRIMARY KEY,
            discussion_id INT,
            user_id INT,
            message TEXT,
            created_at DATETIME,
            categorie VARCHAR(200),
            sous_categorie VARCHAR(200),
            FOREIGN KEY (discussion_id) REFERENCES discussion(pk),
            FOREIGN KEY (user_id) REFERENCES user(pk)
        )
        """
        )
        
        # TABLE PREDICTION "jouer avec l'IA"
        #cursor.execute(
        #    """
        #CREATE TABLE IF NOT EXISTS prediction (
        #    pk INT AUTO_INCREMENT PRIMARY KEY,
        #    title VARCHAR(200) NOT NULL,
        #    message VARCHAR(400) NOT NULL,
        #    categorie VARCHAR(100) NOT NULL,
        #    sous_categorie VARCHAR(100) NOT NULL
        #)
        #"""
        #)

        conn.commit()
        # Fermeture du curseur
        cursor.close()

        print("Base de données et tables créées avec succès !")
        logging.info("Base de données et tables créées avec succès !")

    except mysql.connector.Error as err:
        print(f"Erreur lors de la création de la base de données : {err}")
        logging.error(f"Erreur lors de la création de la base de données : {err}")

    finally:
        # Fermeture de la connexion dans tous les cas
        if conn.is_connected():
            conn.close()


if __name__ == "__main__":
    # Utilisation de la fonction pour configurer le logging
    log_directory = "../../../logs/database_management/database_setup/"
    log_file_name = "database_setup"
    configure_logging(log_directory, log_file_name)

    logging.info("Création de la Base de données...")
    create_database_and_tables()
