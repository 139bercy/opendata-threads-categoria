from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
import os
import pandas as pd
from src.scripts.inference import inference_script
from wtforms.validators import DataRequired

# Importez le module MySQL pour la connexion à la base de données
import mysql.connector
import json
import src.config

# Charger les informations de connexion depuis le fichier de configuration
with open("config.json") as config_file:
    config = json.load(config_file)

# Utilisation des paramètres de connexion
db_host = config["DB_HOST"]
db_user = config["DB_USER"]
db_password = config["DB_PASSWORD"]
db_name = config["DB_NAME"]


class SandboxFormulaire(FlaskForm):
    title = StringField("Titre", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Envoyer")


def process_form(title, message):
    # Créez un DataFrame avec les colonnes correctes
    df = pd.DataFrame({"title_discussion": [title], "message": [message]})

    # Obtenez le chemin du répertoire du script en cours d'exécution
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Spécifiez les noms de fichiers et répertoires relatifs
    model1_zip_file = os.path.join(script_directory, "../../trained_models/bert-finetuned-my-data-final_archive.zip")
    model2_zip_file = os.path.join(script_directory, "../../trained_models/bert-finetuned-my-data-final2_archive2.zip")

    # Chargez et préparez les modèles
    model1, tokenizer1, model2, tokenizer2 = inference_script.load_and_prepare_models(model1_zip_file, model2_zip_file)

    # Effectuez l'inférence avec les modèles
    output_df_model1 = inference_script.perform_inference1(model1, tokenizer1, df)

    # Utilisez la sortie du modèle 1 comme entrée pour le modèle 2
    output_df_model2 = inference_script.perform_inference2(model2, tokenizer2, output_df_model1)

    categorie_predite = output_df_model2["predictions_motifs_label"].to_string(index=False)
    sous_categorie_predite = output_df_model2["predictions_ssmotifs_label"].to_string(index=False)

    print("Les données ont été annotées avec succès !")

    # Insérez les données dans la table 'prediction'
    try:
        conn = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)

        cursor = conn.cursor()

        # Insérez les données dans la table 'prediction'
        query = "INSERT INTO prediction (title, message, categorie, sous_categorie) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, message, categorie_predite, sous_categorie_predite))

        conn.commit()
        print("Données insérées avec succès dans la table 'prediction' !")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion dans la table 'prediction' : {err}")

    finally:
        if conn:
            conn.close()  # Fermeture de la connexion

    # Redirigez l'utilisateur vers une nouvelle page ou faites autre chose selon vos besoins
    return render_template("sandbox_result.html", categorie=categorie_predite, sscategorie=sous_categorie_predite)


def sandbox():
    form = SandboxFormulaire()

    if form.validate_on_submit():
        title = form.title.data
        message = form.message.data

        print(f"Titre: {title}, Message: {message}")

        return process_form(title, message)

    return render_template("sandbox.html", form=form)
