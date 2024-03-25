import logging
import os
import sys

import pandas as pd

sys.path.append("..")
from logging_config import configure_logging


# Obtenez le chemin du dossier du script en cours d'exécution
script_directory = os.path.dirname(__file__)
# Chemin du dossier contenant les fichiers CSV relativement au script
csv_folder_path = os.path.join(script_directory, "../../../data/raw/data_acquisition/")


def load_and_merge_data():
    try:
        # Charger les fichiers CSV
        logging.info("Chargement des fichiers CSV en cours...")
        df_discussions = pd.read_csv(os.path.join(csv_folder_path, "extraction_discussions/discussions.csv"))
        df_datasets = pd.read_csv(os.path.join(csv_folder_path, "extraction_datasets/datasets.csv"))
        df_grp_metiers = pd.read_csv(
            os.path.join(csv_folder_path, "extraction_groupes_metiers/datasets_groupes_metiers_20231030.csv"), sep=";"
        )
        logging.info("Fichiers CSV chargés avec succès.")

        # Fusionner les DataFrames en utilisant les colonnes 'id_subject' et 'id_dataset' comme clés de jointure
        logging.info("Fusion des DataFrames en cours...")
        df_merged = pd.merge(df_discussions, df_datasets, left_on="id_dataset", right_on="id_dataset", how="inner")

        # Ajouter la colonne 'groupe-metier' en fusionnant avec df_grp_metiers
        df_merged = pd.merge(
            df_merged,
            df_grp_metiers[["dataset_id", "groupe-metier"]],
            left_on="slug",
            right_on="dataset_id",
            how="left",
        ).drop("dataset_id", axis=1)
        # df_merged.drop(['dataset_id'], axis=1, inplace=True)  # Drop the duplicate column

        logging.info("Fusion des DataFrames terminée.")

        # Enregistrer le DataFrame fusionné dans un fichier CSV
        merged_csv_path = os.path.join(csv_folder_path, "merging_data/merged_data.csv")
        df_merged.to_csv(merged_csv_path, index=False)
        logging.info("Données fusionnées exportées avec succès au fichier merged_data.csv.")

        return df_merged

    except Exception as e:
        logging.error("Erreur lors du chargement et de la fusion des données : %s", str(e))
        return None


def filter_and_export_data(df_merged):
    # Filtrer le DataFrame MEFSIN en fonction de la colonne 'organization'
    try:
        logging.info("Filtrage des données en cours...")
        df_filtered = df_merged[
            df_merged["organization"]
            == "Ministère de l'Économie, des Finances et de la Souveraineté industrielle et numérique"
        ]
        logging.info("Filtrage des données terminé.")

        # Export des données filtrées au format CSV
        csv_export_path = os.path.join(csv_folder_path, "merging_data/dataset_mefsin.csv")
        df_filtered.to_csv(csv_export_path, index=False)
        logging.info("Données filtrées exportées avec succès au fichier dataset_mefsin.csv.")

    except Exception as e:
        logging.error("Erreur lors du filtrage et de l'export des données : %s", str(e))


if __name__ == "__main__":
    # Utilisation de la fonction pour configurer le logging
    log_directory = "../../../logs/data_acquisition/merging_data/"
    log_file_name = "merging_data"
    configure_logging(log_directory, log_file_name)

    # Chargement et fusion des données
    df_merged = load_and_merge_data()

    if df_merged is not None:
        # Filtrage et export des données
        filter_and_export_data(df_merged)
        logging.info("Les données ont été merge et filtrées avec succès !")
        print("Les données ont été merge et filtrées avec succès !")

    else:
        logging.error("Impossible de continuer sans données valides.")

    # Fermez le système de journalisation
    logging.shutdown()
