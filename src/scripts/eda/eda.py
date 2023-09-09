import pandas as pd
import logging
import os
from datetime import datetime

# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../../../logs/eda'  # Le nom du dossier que vous avez créé
# Générer un nom de fichier de journal unique basé sur la date et l'heure
log_filename = datetime.now().strftime("%Y-%m-%d") + "_eda.log"
# Spécifier le chemin complet du fichier de journal
log_file_path = os.path.join(log_folder_path, log_filename)
# Configurer les paramètres de journalisation avec le chemin complet
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Chargez le fichier CSV généré par le script d'inférence
input_csv_file = '../../../data/raw/inference/predicted_data_model2.csv'
df = pd.read_csv(input_csv_file)

# Nombre total de lignes dans le DataFrame
total_rows = df.shape[0]
print("Nombre total de lignes dans le DataFrame :", total_rows)

# JDD les plus discutés
jdd_counts = df['title_dataset'].value_counts()
#print("JDD les plus discutés :")
#print(jdd_counts)

# JDD avec le plus grand nombre de réutilisations
jdd_reuses = df.groupby('title_dataset')['nb_reuses'].first().sort_values(ascending=False)
#print("JDD avec le plus grand nombre de réutilisations :")
#print(jdd_reuses)

# JDD les plus consultés
jdd_views = df.groupby('title_dataset')['nb_views'].first().sort_values(ascending=False)
#print("JDD les plus consultés :")
#print(jdd_views)

# JDD avec le plus de followers
jdd_followers = df.groupby('title_dataset')['nb_followers'].first().sort_values(ascending=False)
#print("JDD avec le plus de followers :")
#print(jdd_followers)

# Discussions ouvertes/closes
discussions_closes = df['closed'].count()
discussions_ouvertes = total_rows - discussions_closes
print("Nombre de discussions ouvertes :", discussions_ouvertes)
print("Nombre de discussions closes :", discussions_closes)

# Calcul du temps de réponse d'un commentaire entre l'ouverture de la discussion et sa fermeture
df['created'] = pd.to_datetime(df['created'])
df['closed'] = pd.to_datetime(df['closed'])
df['time_response'] = df['closed'] - df['created']

# Calcul de la moyenne des temps de réponse par Annotation
mean_time_response = df.groupby('title_discussion')['time_response'].mean().sort_values(ascending=False)
#print("Moyenne des temps de réponse par Annotation :")
#print(mean_time_response)

logging.INFO("Code executé avec succès !")

# Fermez le fichier de journal
logging.shutdown()
