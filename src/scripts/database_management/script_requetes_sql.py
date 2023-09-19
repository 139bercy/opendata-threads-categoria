import mysql.connector
import os

# Récupérer le host, le nom d'utilisateur et le mot de passe à partir des variables d'environnement
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")

# On s'assure que les variables d'environnement existent
if db_host is None or db_user is None or db_password is None:
    raise Exception("Les variables d'environnement DB_USER et DB_PASSWORD ne sont pas définies.")

# Configuration de la connexion à la base de données
config = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'database': 'database_discussions'
}

# Établir la connexion
conn = mysql.connector.connect(**config)

# Créer un curseur
cursor = conn.cursor()

# Exécuter une requête SQL (exemple : sélectionner toutes les lignes de la table Utilisateur)
query = "SELECT * FROM Utilisateur"
cursor.execute(query)

# Récupérer les résultats
results = cursor.fetchall()

# Afficher les résultats
for row in results:
    print(row)

# Fermer le curseur et la connexion
cursor.close()
conn.close()
