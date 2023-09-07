# Définir les labels
LABELS = ['Fiabilité', 'Autre', 'Actualisation', 'Accessibilité', 'Compréhension', 'Exploitabilité']

# Créer des dictionnaires pour convertir les identifiants de label et les labels
ID2LABEL = {idx:label for idx, label in enumerate(labels)}
LABEL2ID = {label:idx for idx, label in enumerate(labels)}

SSLABELS = ['Incohérence des données',
            "Questions ou remarques d'usagers",
            'Commentaire sans valeur',
            "Erreur d'actualisation",
            'Absence de mise à jour',
            'Erreur dans les données fournies',
            'Lien mort',
            'Format incompatible',
            'Information des réutilisateurs',
            'Absence de description des variables',
            'Absence de données',
            'Demande de jeu de données (set)',
            "Absence d'information sur les mises à jour",
            "Problème d'uniformité dans la saisie",
            'Incertitude des données',
            'Problème de granularité',
            'Proposition de mots-clefs',
            'Incapacité à traiter les données',
            'Formatage non respecté',
            'Source des données incorrecte ou imprécise',
            'Descriptions imprécises',
            'Données non-ouvertes',
            'Répétition des données',
            'Demande de correction',
            'Message automatique',
            'Harmonisation des données']

# Créer des dictionnaires pour convertir les identifiants de label et les labels
ID2SSLABEL = {id:sslabel for id, sslabel in enumerate(sslabels)}
SSLABEL2ID = {sslabel:id for id, sslabel in enumerate(sslabels)}
