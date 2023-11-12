Projet de dashboard d'annotation des discussions autour des jeux de données du Ministère de l'économie et des finances (data.gouv.fr)
==============================

Description du Projet: 
------------
  Ce projet s'inscrit dans le cadre de la mission OpenData du ministère. Il s'agit d'un dashboard qui permettra aux agents du ministère de comprendre quels sont les problèmes que rencontrent les utilisateurs de la plateforme data.gouv.fr avec leurs jeux de données.
Chaque discussion autour des jeux de données sera annoté en une catégorie parmi 6 et une sous catégorie parmi 26 possiblent.
  L'annotation est automatisée grâce à un modèle d'IA de catégorisation basé sur CamemBERT, un modèle largement utilisé dans le domaine du Traitement Automatique du Langage Naturel (NLP).
Le dashboard quant à lui est dévelopé grâce sous Dash plotly.

Fonctionnalités Principales :
------------
- Annotation Automatisée : Le modèle d'IA prend en entrée un texte, composé du titre et de la discussion, et retourne sa classification en catégorie et sous-catégorie.

- Modèle de Catégorisation Imbriqué : Deux modèles CamemBERT sont utilisés. Le premier prédit la catégorie, et le deuxième prédit la sous-catégorie en prenant en entrée la prédiction du premier modèle (catégorie prédite), concaténée avec la discussion et le titre de la discussion pour en prédire la sous catégorie.

- Entraînement Supervisé : Le modèle est entraîné de manière supervisée en s'appuyant sur un échantillon de données préalablement catégorisées manuellement. Nous avons capitalisé pour cela sur les travaux qui ont été réalisés en 2019 par Datactivist pour le compte d'Etalab.

Architecture du Projet
------------
```
projet_discussions/
│
├── data/
│   ├── raw/
│   │   ├── data_acquisition/
│   │   │   ├── datasets.csv          # Résultats du requêtage de l'API pour récupérer les données
│   │   │   ├── discussions.csv       # Discussions extraites des jeux de données
│   │   │   ├── groupes_metier.csv     # Informations sur les groupes métier liés aux discussions
│   │   │   ├── merging_data.csv       # Fusion des datasets et discussions
│   │   │   └── dataset_mefsin.csv     # Données spécifiques au ministère des finances
│   │   └── ...                       # Autres fichiers de sortie .csv
│   │
│   └── ...                           # Autres données traitées ou générées pendant le projet
│
├── logs/
│   ├── ...                           # Fichiers de logs générés par le projet
│   └── ...
│
├── src/
│   ├── notebooks/
│   │   ├── ...                       # Notebooks d'implémentation et d'entraînement du modèle d'IA
│   │   └── ...
│   │
│   ├── scripts/
│   │   ├── ...                       # Scripts Python utilisés dans le projet
│   │   └── ...
│   │
│   └── trained_models/
│       ├── ...                  # Poids des modèles CamemBERT (Modèle 1 : Catégories, Modèle 2 : Sous-catégories)
│       └── ...
│
├── config.json                       # Fichier de configuration des variables d'environnement
└── requirements.txt                  # Liste des dépendances Python nécessaires
```

Instructions d'Utilisation :
------------

- Installation des Dépendances : Exécuter pip install -r requirements.txt pour installer les librairies requises.
- Exécution des Scripts : Utiliser les scripts et notebooks dans le dossier src/ pour exécuter différentes parties du projet.
- Configuration : Modifier le fichier config.json pour ajuster les variables d'environnement au besoin.

Remarques :
- Assurez-vous d'avoir les autorisations nécessaires pour accéder aux données et effectuer des requêtes API.
- Les modèles entraînés sont stockés dans le dossier trained_models/.
- Les résultats des requêtes API sont disponibles dans le dossier data/raw/data_acquisition/.
