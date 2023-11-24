import pandas as pd
import logging
import os
from datetime import datetime
import dash
from dash import dcc, html
import plotly.express as px

# Charger le fichier CSV généré par le script d'inférence
input_csv_file = '../../../data/raw/inference/predicted_data_model2.csv'
df = pd.read_csv(input_csv_file)

# Configurer les paramètres de journalisation
log_folder_path = '../../../logs/eda'
log_filename = datetime.now().strftime("%Y-%m-%d") + "_eda.log"
log_file_path = os.path.join(log_folder_path, log_filename)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Calculer le nombre total de lignes dans le DataFrame
total_rows = df.shape[0]
logging.info(f"Nombre total de lignes dans le DataFrame : {total_rows}")

# Calculer les JDD les plus discutés
jdd_counts = df['slug'].value_counts()
# Trier par ordre décroissant
jdd_counts = jdd_counts.sort_values(ascending=False)
logging.info("JDD les plus discutés :")
# logging.info(jdd_counts)

# Calculer les JDD avec le plus grand nombre de réutilisations
jdd_reuses = df.groupby('title_dataset')['nb_reuses'].first().sort_values(ascending=False)
logging.info("JDD avec le plus grand nombre de réutilisations :")
#logging.info(jdd_reuses)

# Calculer les JDD les plus consultés
jdd_views = df.groupby('title_dataset')['nb_views'].first().sort_values(ascending=False)
logging.info("JDD les plus consultés :")
#logging.info(jdd_views)

# Calculer les JDD avec le plus de followers
jdd_followers = df.groupby('title_dataset')['nb_followers'].first().sort_values(ascending=False)
logging.info("JDD avec le plus de followers :")
#logging.info(jdd_followers)

# Calculer le nombre de discussions ouvertes et fermées
discussions_closes = pd.to_datetime(df['closed_discussion'], format='%d/%m/%Y', errors='coerce').count()
discussions_ouvertes = total_rows - discussions_closes
logging.info(f"Nombre de discussions ouvertes : {discussions_ouvertes}")
logging.info(f"Nombre de discussions closes : {discussions_closes}")

# Calcul du temps de réponse d'un commentaire entre l'ouverture de la discussion et sa fermeture
df['created'] = pd.to_datetime(df['created_discussion'], format='%d/%m/%Y', errors='coerce')
df['closed'] = pd.to_datetime(df['closed_discussion'], format='%d/%m/%Y', errors='coerce')
df['time_response'] = df['closed'] - df['created']

# Calculer la moyenne des temps de réponse par annotation
mean_time_response = df.groupby('title_discussion')['time_response'].mean().sort_values(ascending=False)
logging.info("Moyenne des temps de réponse par annotation :")
logging.info(mean_time_response)

# Fermer le fichier de journal
logging.shutdown()

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Mise en page de l'application
app.layout = html.Div([
    html.H1("Dashboard for Discussion Data"),

    # Graphique en barres des JDD les plus discutés
    dcc.Graph(
        id='bar-chart-jdd-discutes',
        figure=px.bar(
            y=jdd_counts.index,
            x=jdd_counts.values,
            orientation='h',
            title='JDD les plus discutés',
            category_orders={'y': list(jdd_counts.index)},  # Inverser l'ordre
            text=jdd_counts.values,  # Texte à afficher à côté des barres
            labels={'x': 'Nombre de Discussions', 'y': 'Slug jdd'},  # Libellés des axes
            height=800,  # Hauteur du graphique
            width=1200,  # Largeur du graphique
        )
    ),

    # Graphique circulaire (pie chart) pour la proportion de discussions ouvertes et fermées
    dcc.Graph(
        id='pie-chart-discussions',
        figure=px.pie(
            names=['Discussions Ouvertes', 'Discussions Closes'],
            values=[discussions_ouvertes, discussions_closes],
            title='Proportion de Discussions Ouvertes et Closes',
            color_discrete_sequence=['#ED4646', '#33BB5C'],
            hole=0.4,
        ).update_traces(
        texttemplate="<b>%{percent:.0%}</b>",  # Utiliser HTML pour mettre en gras      
        insidetextfont=dict(size=16), 
    )
    ),
])

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
