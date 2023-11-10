import mysql.connector
import logging
import os
import json
from datetime import datetime

import sys
sys.path.append('..')
from logging_config import configure_logging

"""# Vérification et création du répertoire de logs
def configure_logging(log_directory, log_file_name):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    # Configuration du logging
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    log_file = os.path.join(log_directory, f"{log_file_name}_{timestamp}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')"""

# Récupérer le host, le nom d'utilisateur et le mot de passe à partir des variables d'environnement situées dans le fichier de conf.
def load_db_config():
    with open('../../../config.json') as config_file:
        return json.load(config_file)

def create_database_and_tables():
    config = load_db_config()

    db_host = config['DB_HOST']
    db_user = config['DB_USER']
    #db_password = config['DB_PASSWORD']
    #db_name = config['DB_NAME']

    try:
        # Connexion à MySQL avec les paramètres chargés depuis le fichier de configuration
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            #password=db_password
        )
        
        cursor = conn.cursor()
        
        # Création de la base de données
        cursor.execute("CREATE DATABASE IF NOT EXISTS database_discussions")

        """# Fermeture du curseur
        cursor.close()
        conn.close()

        # Connexion à la base de données nouvellement créée
        conn = mysql.connector.connect(
            host= db_host,
            user= db_user,
            password= db_password,
            database="database_discussions"
        )"""

        # Utilisation de la base de données nouvellement créée
        cursor.execute("USE database_discussions")
        
        # Création de tables (Utilisateur, Discussion, Dataset)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            pk INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Organizations (
            id_organization INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Datasets (
            id_data INT AUTO_INCREMENT PRIMARY KEY,
            id_dataset VARCHAR(50) NOT NULL UNIQUE,
            title VARCHAR(400),
            description TEXT,
            url VARCHAR(400),
            created DATETIME,
            last_update DATETIME,
            slug VARCHAR(255) NOT NULL UNIQUE,
            nb_discussions INT,
            nb_followers INT,
            nb_reuses INT,
            nb_views INT, 
            id_organization INT,
            FOREIGN KEY (id_organization) REFERENCES Organizations(id_organization)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Discussions (
            id_disc INT AUTO_INCREMENT PRIMARY KEY,
            id_discussion VARCHAR(50) NOT NULL UNIQUE,
            created DATETIME,
            closed DATETIME,
            title VARCHAR(400),
            id_data INT,
            FOREIGN KEY (id_data) REFERENCES Datasets(id_data)
        )
        """)
        
        #Table intermédiaire car relation (n,n)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Messages (
            id_message INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            posted_on DATETIME,
            id_disc INT,
            id_user INT,
            FOREIGN KEY (id_disc) REFERENCES Discussions(id_disc),
            FOREIGN KEY (id_user) REFERENCES Users(id_user)
        )
        """)

        # Fermeture du curseur et de la connexion
        cursor.close()
        conn.close()

        print("Base de données et tables créées avec succès !")
        # Logging : Enregistrement d'un message de succès
        logging.info("Base de données et tables créées avec succès !")

    except mysql.connector.Error as err:
        print(f"Erreur lors de la création de la base de données : {err}")
        # Logging : Enregistrement d'une erreur
        logging.error(f"Erreur lors de la création de la base de données : {err}")

if __name__ == "__main__":
    # Utilisation de la fonction pour configurer le logging
    log_directory = "../../../logs/database_management/database_setup/"
    log_file_name = 'database_setup'
    configure_logging(log_directory, log_file_name)

    logging.info("Création de la Base de données...")
    create_database_and_tables()
