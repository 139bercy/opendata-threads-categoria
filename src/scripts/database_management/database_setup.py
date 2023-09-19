import mysql.connector
import logging
import os

# Vérification et création du répertoire de logs
log_directory = "../../../logs/database_management/"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration du logging
log_file = os.path.join(log_directory, 'database_setup.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Récupérer le host, le nom d'utilisateur et le mot de passe à partir des variables d'environnement
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")

# On s'assure que les variables d'environnement existent
if db_host is None or db_user is None or db_password is None:
    raise Exception("Les variables d'environnement DB_USER et DB_PASSWORD ne sont pas définies.")

def create_database_and_tables():
    try:
        # Connexion à MySQL
        conn = mysql.connector.connect(
            host= db_host,
            user= db_user,
            password= db_password
        )

        # Création de la base de données
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS database_discussions")

        # Fermeture du curseur
        cursor.close()
        conn.close()

        # Connexion à la base de données nouvellement créée
        conn = mysql.connector.connect(
            host= db_host,
            user= db_user,
            password= db_password,
            database="database_discussions"
        )

        # Création de tables (Utilisateur, Discussion, Dataset)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Utilisateur (
            user VARCHAR(255) PRIMARY KEY
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dataset (
            id_dataset INT PRIMARY KEY,
            title_dataset VARCHAR(255),
            description_dataset TEXT,
            organization VARCHAR(255),
            url_dataset VARCHAR(255),
            created_dataset DATE,
            last_update_dataset DATE,
            slug VARCHAR(255),
            nb_discussions INT,
            nb_followers INT,
            nb_reuses INT,
            nb_views INT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Discussion (
            id_discussion INT PRIMARY KEY,
            created_discussion DATETIME,
            closed_discussion DATETIME,
            discussion_posted_on DATE,
            title_discussion VARCHAR(255),
            message TEXT,
            user VARCHAR(255),
            id_dataset INT,
            FOREIGN KEY (user) REFERENCES Utilisateur(user),
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
