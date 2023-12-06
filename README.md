# Open Thread CategorIA

_Tableau de bord d'annotation des discussions autour des jeux de données du Ministère de l'économie et des
finances (data.gouv.fr)_

## Description du projet

Ce projet s'inscrit dans le cadre de la mission OpenData du ministère.
Il s'agit d'un tableau de bord qui permettra aux agents du ministère de comprendre quels sont les problèmes que
rencontrent les utilisateurs de la plateforme data.gouv.fr avec leurs jeux de données.
Chaque discussion autour des jeux de données sera annotée en une catégorie parmi 6 et une sous catégorie parmi 26
possibles.

L'annotation est automatisée grâce à un modèle d'IA de catégorisation basé sur CamemBERT, un modèle largement utilisé
dans le domaine du Traitement Automatique du Langage Naturel (NLP).
Le dashboard quant à lui est développé avec Dash plotly.

## Fonctionnalités Principales

- Annotation Automatisée : Le modèle d'IA prend en entrée un texte, composé du titre et de la discussion, et retourne sa
  classification en catégorie et sous-catégorie.
- Modèle de Catégorisation Imbriqué : Deux modèles CamemBERT sont utilisés. Le premier prédit la catégorie, et le
  deuxième prédit la sous-catégorie en prenant en entrée la prédiction du premier modèle (catégorie prédite), concaténée
  avec la discussion et le titre de la discussion pour en prédire la sous catégorie.
- Entraînement Supervisé : Le modèle est entraîné de manière supervisée en s'appuyant sur un échantillon de données
  préalablement catégorisées manuellement. Nous avons capitalisé pour cela sur les travaux qui ont été réalisés en 2019
  par Datactivist pour le compte d'Etalab.

## Architecture du Projet

### Entrypoints

- API pilotée par Flask
- Système de gestion en lignes de commande (CLI)

### Applications :

- `auth` : gestionnaire d'authentification basique
  - `thread` : gestionnaire de discussions et coeur de l'application. TODO: Renommer `core`.

Les applications suivent la même arborescence :

- `exceptions` : les exceptions métier levées par les différents cas d'usage.
- `gateways` : les contrats (sous forme d'Abstract Base Class en Python) passés avec les dépendances.
- `infrastructure` : les repositories, qui héritent des contrats définis dans `gateways`
- `models` : les objets de base (écrits en Python) qui circulent entre les couches.
- `usecases` : fonctions utilisées par les `entrypoints` qui permettent de traiter les cas d'usage

## Installation

Modifiez le contenu des variables d'environnement selon vos usages.

```
$ cp .env.sampla .env
$ make install
```

## Instructions d'Utilisation

- Installation des Dépendances : Exécuter pip install -r requirements.txt pour installer les librairies requises.
- Exécution des Scripts : Utiliser les scripts et notebooks dans le dossier src/ pour exécuter différentes parties du
  projet.
- Configuration : Modifier le fichier config.json pour ajuster les variables d'environnement au besoin.

Remarques :

- Assurez-vous d'avoir les autorisations nécessaires pour accéder aux données et effectuer des requêtes API.
- Les modèles entraînés sont stockés dans le dossier trained_models/.
- Les résultats des requêtes API sont disponibles dans le dossier data/raw/data_acquisition/.

## Usage

Pour lancer le front-end, d'un environnement virtuel :

```
$ python app.py
```

Pour interagir en lignes de commande :

```
$ python commands.py
```

### Dev

Pré-requis : avoir installé Docker et docker-compose.
Les commandes liées sont dans le fichier `Makefile`.
