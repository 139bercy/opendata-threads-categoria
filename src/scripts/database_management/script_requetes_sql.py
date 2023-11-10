import mysql.connector
import os
import json
import logging
import pandas as pd

import sys
sys.path.append('..')
from logging_config import configure_logging

# Charger les informations de connexion depuis le fichier de configuration
with open('../../../config.json') as config_file:
    config = json.load(config_file)
    
# Connexion à la base de données
# Utilisation des paramètres de connexion
db_host = config['DB_HOST']
db_user = config['DB_USER']
#db_password = config['DB_PASSWORD']
db_name = config['DB_NAME']
            
def fetch_messages_ordered():
    conn = None
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            # password=db_password,
            database="database_discussions"
        )
        
        if conn.is_connected():
            cursor = conn.cursor()

            # Exécuter la requête SQL pour récupérer les messages
            query = "SELECT * FROM Messages ORDER BY id_disc ASC, posted_on ASC;"
                    #"SELECT * FROM Messages GROUP BY id_disc ORDER BY id_disc ASC, posted_on ASC;"
            cursor.execute(query)

            # Récupérer les résultats
            messages = cursor.fetchall()

            # Afficher les messages
            #for message in messages:
            #    print(message)  # Adapter pour afficher les colonnes souhaitées"""
                
            # Créer un DataFrame pandas avec les résultats
            df = pd.DataFrame(messages, columns=[i[0] for i in cursor.description])

            # Afficher le DataFrame pandas
            print(df)
            
            # Save the DataFrame to CSV
            df.to_csv("groupedby_id_discussion.csv", index=False)

    except mysql.connector.Error as e:
        print(f"Erreur : {e}")
        logging.error(f"Erreur : {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Utilisation de la fonction pour configurer le logging
    log_directory = "../../../logs/database_management/data_to_database/"
    log_file_name = 'script-requetes_sql.py'
    configure_logging(log_directory, log_file_name)
        
    # Utilisation de la fonction pour récupérer et afficher les discussions ordonnées
    fetch_messages_ordered()
