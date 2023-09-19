import mysql.connector
import pandas as pd

def import_data_from_csv():
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bercy_Hub",
            database="database_discussions"
        )

        # Charger les données CSV dans un DataFrame
        data = pd.read_csv("../../../data/raw/data_acquisition/merging_data/dataset_mefsin.csv.csv")

        # Créer un curseur
        cursor = conn.cursor()

        # Itérer sur les lignes du DataFrame et insérer les données dans la table Utilisateur
        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO Utilisateur (user)
            VALUES (%s)
            """, (row["user"],))

            # Insérer des données dans la table Discussion
            cursor.execute("""
            INSERT INTO Discussion (created_discussion, closed_discussion, discussion_posted_on, title_discussion, message, user, id_dataset)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (row["created_discussion"], row["closed_discussion"], row["discussion_posted_on"], row["title_discussion"], row["message"], row["user"], row["id_dataset"]))

            # Insérer des données dans la table Dataset
            cursor.execute("""
            INSERT INTO Dataset (title_dataset, description_dataset, organization, url_dataset, created_dataset, last_update_dataset, slug, nb_discussions, nb_followers, nb_reuses, nb_views)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row["title_dataset"], row["description_dataset"], row["organization"], row["url_dataset"], row["created_dataset"], row["last_update_dataset"], row["slug"], row["nb_discussions"], row["nb_followers"], row["nb_reuses"], row["nb_views"]))

        # Valider les changements et fermer la connexion
        conn.commit()
        conn.close()

        print("Données CSV importées avec succès dans les tables.")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'importation des données CSV : {err}")

if __name__ == "__main__":
    import_data_from_csv()
