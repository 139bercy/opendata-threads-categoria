import mysql.connector
import logging
import os
import json

# Vérification et création du répertoire de logs
log_directory = "../../../logs/database_management/"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration du logging
log_file = os.path.join(log_directory, 'database_setup.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        CREATE TABLE IF NOT EXISTS Utilisateur (
            id_user INT AUTO_INCREMENT PRIMARY KEY, (voir pour ajouter le vrai user_id de la requete api)
            user VARCHAR(100) 
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Organization (
            id_organization INT AUTO_INCREMENT PRIMARY KEY,
            organization VARCHAR(100)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dataset (
            id_dataset INT NOT NULL PRIMARY KEY,
            title_dataset VARCHAR(100),
            description_dataset TEXT,
            url_dataset VARCHAR(100),
            created_dataset DATE,
            last_update_dataset DATE, (datetimestemp)
            slug VARCHAR(100),
            nb_discussions INT,
            nb_followers INT,
            nb_reuses INT,
            nb_views INT, 
            id_organization INT,
            FOREIGN KEY (id_organization) REFERENCES Organization(id_organization)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Discussion (
            id_discussion INT NOT NULL PRIMARY KEY,
            created_discussion DATETIME,
            closed_discussion DATETIME,
            discussion_posted_on DATE,
            title_discussion VARCHAR(100),
            message TEXT,
            id_user VARCHAR(100),
            id_dataset INT,
            FOREIGN KEY (user) REFERENCES Utilisateur(id_user),
            FOREIGN KEY (id_dataset) REFERENCES Dataset(id_dataset)
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
    logging.info("Création de la Base de données...")
    create_database_and_tables()
