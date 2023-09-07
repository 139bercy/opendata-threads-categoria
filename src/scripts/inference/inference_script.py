import zipfile
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
import re
from datetime import datetime
import os
import categories
from preprocess import preprocess_data, preprocess_data2

# Spécifier le chemin relatif vers le dossier logs
log_folder_path = '../logs/inference'  # Le nom du dossier que vous avez créé
# Générer un nom de fichier de journal unique basé sur la date et l'heure
log_filename = datetime.now().strftime("%Y-%m-%d") + "_inference.log"
# Spécifier le chemin complet du fichier de journal
log_file_path = os.path.join(log_folder_path, log_filename)
# Configurer les paramètres de journalisation avec le chemin complet
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Accédez aux dictionnaires définis dans categories.py
labels = categories.labels
id2label = categories.id2label
label2id = categories.label2id

sslabels = categories.sslabels
id2sslabel = categories.id2sslabel
sslabel2id = categories.sslabel2id

def load_and_prepare_models(model1_zip, model2_zip):
    # Charger du model 1 pré-entrainé (zippé)
    # Extraire le contenu du fichier .zip dans un répertoire temporaire
    extract_dir1 = "../models/extracted_model"
    with zipfile.ZipFile(model1_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir1)
    logging.info("Modèle 1 extrait avec succès dans %s", extract_dir1)

    # Charger le modèle à partir du répertoire extrait
    model_saved1 = AutoModelForSequenceClassification.from_pretrained(extract_dir1)

    # Charger le tokenizer à partir du même répertoire extrait
    tokenizer_saved1 = AutoTokenizer.from_pretrained(extract_dir1)

    # Chargement du modèle 2 (zippé)
    # Extraire le contenu du fichier .zip dans un répertoire temporaire
    extract_dir2 = "../models/extracted_model2"
    with zipfile.ZipFile(model2_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir2)
    logging.info("Modèle 2 extrait avec succès dans %s", extract_dir2)

    # Charger le modèle à partir du répertoire extrait
    model_saved2 = AutoModelForSequenceClassification.from_pretrained(extract_dir2)

    # Charger le tokenizer à partir du même répertoire extrait
    tokenizer_saved2 = AutoTokenizer.from_pretrained(extract_dir2)

    return model_saved1, tokenizer_saved1, model_saved2, tokenizer_saved2


def perform_inference1(model1, tokenizer1, csv_file_path, output_csv_path):
    # Début de l'inférence 1
    logging.info("Début de l'inférence 1 ...")
    
    # Charger le DataFrame
    df_MEFSIN = pd.read_csv(csv_file_path)
    logging.info("Chargement du DataFrame effectué avec succès !")

    # Prétraitement des données
    preprocessed_data = preprocess_data(df_MEFSIN)

    # Vérifier si preprocessed_data est None
    if preprocessed_data is None:
        logging.error("La fonction preprocess_data a renvoyé None. Veuillez vérifier la fonction.")
        raise ValueError("La fonction preprocess_data a renvoyé None. Veuillez vérifier la fonction.")

    logging.info("Inférence (1) en cours ...")
    # Créer une liste pour stocker les prédictions du modèle 1
    predictions1 = []

    # Définir la taille du batch d'inférence
    batch_size = 16

    # Diviser les données en lots plus petits
    num_batches = len(preprocessed_data) // batch_size
    if len(preprocessed_data) % batch_size != 0:
        num_batches += 1

    # Mettre le modèle 1 en mode évaluation
    model1.eval()

    # Parcourir les lots et effectuer l'inférence avec le modèle 1
    for i in range(num_batches):
        # Sélectionner les textes du lot actuel
        batch_texts = preprocessed_data[i * batch_size: (i + 1) * batch_size]

        # Appliquer le tokenizer et le modèle 1 pour l'inférence
        with torch.no_grad():
            # Encoder les textes avec le tokenizer
            encoded_inputs = tokenizer1(
                batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt"
            )

            # Passage des données dans le modèle 1 pour l'inférence
            outputs = model1(input_ids=encoded_inputs['input_ids'], attention_mask=encoded_inputs['attention_mask'])

        # Récupération des prédictions
        predicted_labels = torch.argmax(outputs.logits, dim=1)

        # Ajouter les prédictions à la liste des résultats du modèle 1
        predictions1.extend(predicted_labels.tolist())

    # Ajouter la liste des prédictions du modèle 1 comme une nouvelle colonne au DataFrame
    df_MEFSIN['predictions_motifs'] = predictions1
    df_MEFSIN['predictions_motifs_label'] = [id2label[prediction] for prediction in predictions1]
    
    # Sauvegarder le DataFrame avec les prédictions dans un fichier CSV
    df_MEFSIN.to_csv(output_csv_path, index=False)

    logging.info("Inférence avec le modèle 1 terminée et résultats sauvegardés dans %s", output_csv_path)


def perform_inference2(model2, tokenizer2, csv_file_path, output_csv_path):
    # Début de l'inférence 1
    logging.info("Début de l'inférence 2 ...")
    
    # Charger le DataFrame
    df_MEFSIN = pd.read_csv(csv_file_path)
    logging.info("Chargement du DataFrame effectué avec succès !")

    # Prétraitement des données pour le modèle 2
    preprocessed_data2 = preprocess_data2(df_MEFSIN)

    # Vérifier si preprocessed_data2 est None
    if preprocessed_data2 is None:
        logging.error("La fonction preprocess_data2 a renvoyé None. Veuillez vérifier la fonction.")
        raise ValueError("La fonction preprocess_data2 a renvoyé None. Veuillez vérifier la fonction.")

    logging.info("Inférence (2) en cours ...")
    # Créer une liste pour stocker les prédictions du modèle 2
    predictions2 = []

    # Définir la taille du batch d'inférence
    batch_size = 16

    # Diviser les données en lots plus petits
    num_batches = len(preprocessed_data2) // batch_size
    if len(preprocessed_data2) % batch_size != 0:
        num_batches += 1

    # Mettre le modèle 2 en mode évaluation
    model2.eval()

    # Parcourir les lots et effectuer l'inférence avec le modèle 2
    for i in range(num_batches):
        # Sélectionner les textes du lot actuel
        batch_texts = preprocessed_data2[i * batch_size: (i + 1) * batch_size]

        # Appliquer le tokenizer et le modèle 2 pour l'inférence
        with torch.no_grad():
            # Encoder les textes avec le tokenizer
            encoded_inputs2 = tokenizer2.batch_encode_plus(batch_texts, truncation=True, padding=True, max_length=128, return_tensors="pt")

            # Passage des données dans le modèle 2 pour l'inférence
            outputs2 = model2(**encoded_inputs2)

        # Récupération des prédictions
        predicted_sslabels = torch.argmax(outputs2.logits, dim=1)

        # Ajouter les prédictions à la liste des résultats du modèle 2
        predictions2.extend(predicted_sslabels.tolist())

    # Ajouter la liste des prédictions du modèle 2 comme une nouvelle colonne au DataFrame
    df_MEFSIN['predictions_ssmotifs'] = predictions2
    df_MEFSIN['predictions_ssmotifs_label'] = [id2sslabel[prediction] for prediction in predictions2]
    # Ajouter une colonne 'predictions_ssmotifs_label' avec les noms de labels correspondant
    #df_MEFSIN['predictions_ssmotifs_label'] = df_MEFSIN['predictions_ssmotifs'].map(id2sslabel)

    
    # Sauvegarder le DataFrame avec les prédictions dans un fichier CSV
    df_MEFSIN.to_csv(output_csv_path, index=False)

    logging.info("Inférence avec le modèle 2 terminée et résultats sauvegardés dans %s", output_csv_path)
    

if __name__ == "__main__":
    # Obtenez le chemin du répertoire du script en cours d'exécution
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Spécifiez les noms de fichiers et répertoires relatifs
    model1_zip_file = os.path.join(script_directory, "../models/bert-finetuned-my-data-final_archive.zip")
    model2_zip_file = os.path.join(script_directory, "../models/bert-finetuned-my-data-final2_archive2.zip")
    input_csv_file1 = os.path.join(script_directory, "../data/raw/merging/merged_data.csv")
    input_csv_file2 = os.path.join(script_directory, "../data/raw/inference/predicted_data_model1.csv")
    output_csv_file_model1 = os.path.join(script_directory, "../data/raw/inference/predicted_data_model1.csv")
    output_csv_file_model2 = os.path.join(script_directory, "../data/raw/inference/predicted_data_model2.csv")

    # Chargez et préparez les modèles
    model1, tokenizer1, model2, tokenizer2 = load_and_prepare_models(model1_zip_file, model2_zip_file)

    # Effectuez l'inférence avec les modèles
    perform_inference1(model1, tokenizer1, input_csv_file1, output_csv_file_model1)
    perform_inference2(model2, tokenizer2, input_csv_file2, output_csv_file_model2)
    
    # Fermez le système de journalisation
    logging.shutdown()