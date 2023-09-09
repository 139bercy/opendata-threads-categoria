import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
import logging
from datetime import datetime
import os

nltk.download('stopwords')

# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../../../logs/inference'  # Le nom du dossier que vous avez créé
# Générer un nom de fichier de journal unique basé sur la date et l'heure
log_filename = datetime.now().strftime("%Y-%m-%d") + "_preprocessing.log"
# Spécifier le chemin complet du fichier de journal
log_file_path = os.path.join(log_folder_path, log_filename)
# Configurer les paramètres de journalisation avec le chemin complet
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Obtenez le chemin du dossier du script en cours d'exécution
script_directory = os.path.dirname(__file__)
# Chemin du dossier contenant les fichiers CSV relativement au script
csv_folder_path = os.path.join(script_directory, '../../../data/raw/')

# Charger le fichier CSV
df_MEFSIN = pd.read_csv(os.path.join(csv_folder_path, 'data_acquisition/dataset_MEFSIN.csv'))

# LABEL
# df_MEFSIN['combined_text'] = df_MEFSIN['title_discussion'] + ' ' + df_MEFSIN['message']

# Fonction de prétraitement pour encoder les exemples et ajouter les labels
def preprocess_data(examples):
    try:
        logging.info("Prétraitement des données (1) en cours...")
        combined_text = examples["title_discussion"] + ' ' + examples["message"]
        
        # Nettoyage du texte
        #combined_text = examples["combined_text"]
        # Convertir chaque texte en minuscules
        combined_text = [text.lower() for text in combined_text]
        # Supprimer les chiffres
        combined_text = [re.sub(r'\d+', '', text) for text in combined_text]
        # Supprimer les adresses mail
        combined_text = [re.sub(r'\S+@\S+', '', text) for text in combined_text]
        # Supprimer les caractères de ponctuation sauf les apostrophes et les accents
        combined_text = [re.sub(r"[^\w\s'-.]", '', text) for text in combined_text]
        # Supprimer certains mots vides
        words_to_remove = ['bonjour', 'bonsoir', 'bonne journée', 'cordialement', 'merci', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'aout', 'septembre', 'octobre', 'novembre', 'décembre']
        combined_text = [[word for word in text.split() if word not in words_to_remove] for text in combined_text]
        combined_text = [' '.join(text) for text in combined_text]
        # Supprimer les espaces en trop et les sauts de lignes
        combined_text = [re.sub(r'\s+', ' ', text) for text in combined_text]
        combined_text = [text.strip() for text in combined_text]
        logging.info("Prétraitement des données terminé (1).")
        
        return combined_text
    
    except Exception as e:
        logging.error("Erreur lors du prétraitement des données : %s", str(e))
        return None
    

# SOUS LABEL
# df_MEFSIN['combined_text_2'] = df_MEFSIN['predictions_motifs_label'] + ' ' + df_MEFSIN['predictions_motifs_label'] + ' ' + df_MEFSIN['predictions_motifs_label'] + ' ' + df_MEFSIN['title_discussion'] + ' ' + df_MEFSIN['message']

# Fonction de prétraitement pour encoder les exemples et ajouter les labels
def preprocess_data2(examples):
    try:
        logging.info("Prétraitement des données (2) en cours...")
        combined_text2 = examples["predictions_motifs_label"] + ' ' + examples["title_discussion"] + ' ' + examples["message"]
        
        # Nettoyage du texte
        #combined_text2 = examples["combined_text_2"]
        # Convertir chaque texte en minuscules
        combined_text2 = [text.lower() for text in combined_text2]
        # Supprimer les chiffres
        combined_text2 = [re.sub(r'\d+', '', text) for text in combined_text2]
        # Supprimer les adresses mail
        combined_text2 = [re.sub(r'\S+@\S+', '', text) for text in combined_text2]
        # Supprimer les caractères de ponctuation sauf les apostrophes et les accents
        combined_text2 = [re.sub(r"[^\w\s'-.]", '', text) for text in combined_text2]
        # Supprimer certains mots vides
        words_to_remove = ['bonjour', 'bonsoir', 'bonne journée', 'cordialement', 'merci', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'aout', 'septembre', 'octobre', 'novembre', 'décembre']
        combined_text2 = [[word for word in text.split() if word not in words_to_remove] for text in combined_text2]
        combined_text2 = [' '.join(text) for text in combined_text2]
        # Supprimer les espaces en trop et les sauts de lignes
        combined_text2 = [re.sub(r'\s+', ' ', text) for text in combined_text2]
        combined_text2 = [text.strip() for text in combined_text2]     
        logging.info("Prétraitement des données (2) terminé.") 
        
        return combined_text2
    
    except Exception as e:
        logging.error("Erreur lors du prétraitement des données (2) : %s", str(e))
        return None
    
    
# Fermez le système de journalisation
logging.shutdown()
