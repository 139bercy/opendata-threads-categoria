import mysql.connector

# Configuration de la connexion à la base de données
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'BercyHub2023',
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
