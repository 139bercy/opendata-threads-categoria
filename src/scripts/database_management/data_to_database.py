import mysql.connector
import pandas as pd
import logging
import os
from datetime import datetime
from dateutil import parser

# Configuration du logging
log_directory = "../../../logs/data_management/"
log_file = os.path.join(log_directory, 'data_to_database.log')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def import_data_from_csv():
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="BercyHub2023",
            database="database_discussions"
        )

        # Charger les données CSV dans un DataFrame
        data = pd.read_csv("../../../data/raw/data_acquisition/merging_data/dataset_mefsin.csv")

        # Créer un curseur
        cursor = conn.cursor()

        # Itérer sur les lignes du DataFrame et insérer les données dans la table Utilisateur
        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO Utilisateur (user)
            VALUES (%s)
            """, (row["user"],))
            
            # Supprimer la partie du fuseau horaire et convertir la date
            original_date = '2023-09-13T09:04:58.310000+0000'
            date_without_timezone = original_date.split('+')[0]  # Supprime le fuseau horaire
            formatted_last_update_date = datetime.strptime(date_without_timezone, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')

            # Insérer des données dans la table Dataset
            cursor.execute("""
            INSERT INTO Dataset (title_dataset, description_dataset, organization, url_dataset, created_dataset, last_update_dataset, slug, nb_discussions, nb_followers, nb_reuses, nb_views)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row["title_dataset"], row["description_dataset"], row["organization"], row["url_dataset"], row["created_dataset"], row["last_update_dataset"], row["slug"], row["nb_discussions"], row["nb_followers"], row["nb_reuses"], row["nb_views"]))

            # Insérer des données dans la table Discussion
            cursor.execute("""
            INSERT INTO Discussion (created_discussion, closed_discussion, discussion_posted_on, title_discussion, message, user, id_dataset)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (row["created_discussion"], row["closed_discussion"], row["discussion_posted_on"], row["title_discussion"], row["message"], row["user"], row["id_dataset"]))

        # Valider les changements et fermer la connexion
        conn.commit()
        conn.close()

        print("Données CSV importées avec succès dans les tables !")
        # Logging : Enregistrement d'un message de succès
        logging.info("Données CSV importées avec succès dans les tables !")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'importation des données CSV : {err}")
        # Logging : Enregistrement d'une erreur
        logging.error(f"Erreur lors de l'importation des données CSV : {err}")

if __name__ == "__main__":
    logging.info("Importation des données csv et remplissage des tables...")
    import_data_from_csv()
