import pandas as pd
import logging
import os
from datetime import datetime
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go  # Importer la bibliothèque plotly.graph_objects

# Charger le fichier CSV généré par le script d'inférence
input_csv_file = "../../data/raw/inference/predicted_data_model2.csv"
df = pd.read_csv(input_csv_file)

# Calculer le nombre total de lignes dans le DataFrame
total_rows = df.shape[0]

# Calculer les JDD les plus discutés
jdd_counts = df["slug"].value_counts()
# Trier par ordre décroissant
jdd_counts = jdd_counts.sort_values(ascending=False)

# Calculer les JDD avec le plus grand nombre de réutilisations
jdd_reuses = df.groupby("title_dataset")["nb_reuses"].first().sort_values(ascending=False)

# Calculer les JDD les plus consultés
jdd_views = df.groupby("title_dataset")["nb_views"].first().sort_values(ascending=False)

# Calculer les JDD avec le plus de followers
jdd_followers = df.groupby("title_dataset")["nb_followers"].first().sort_values(ascending=False)

# Calculer le nombre de discussions ouvertes et fermées
discussions_closes = pd.to_datetime(df["closed_discussion"], format="%d/%m/%Y", errors="coerce").count()
discussions_ouvertes = total_rows - discussions_closes

# Calcul du temps de réponse d'un commentaire entre l'ouverture de la discussion et sa fermeture
df["created"] = pd.to_datetime(df["created_discussion"], format="%d/%m/%Y", errors="coerce")
df["closed"] = pd.to_datetime(df["closed_discussion"], format="%d/%m/%Y", errors="coerce")
df["time_response"] = df["closed"] - df["created"]

# Calculer la moyenne des temps de réponse par annotation
mean_time_response = df.groupby("title_discussion")["time_response"].mean().sort_values(ascending=False)

# Calculer le nombre total de discussions
total_discussions = total_rows

# Calculer le temps de réponse moyen total
mean_time_response_total = df["time_response"].mean()

# Calculer la médiane des temps de réponse par annotation
median_time_response = df.groupby("title_discussion")["time_response"].median().sort_values(ascending=False)

# Calculer le temps de réponse moyen total
median_time_response_total = df["time_response"].median()

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Mise en page de l'application
app.layout = html.Div(
    [
        html.H1("Dashboard for Discussion Data"),
        # Ajout des KPIs
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Total Discussions"),
                        html.H4(total_discussions),
                    ],
                    className="kpi-card",
                ),
                html.Div(
                    [
                        html.H3("Open Discussions"),
                        html.H4(discussions_ouvertes),
                    ],
                    className="kpi-card",
                ),
                html.Div(
                    [
                        html.H3("Mean Time Response (Total)"),
                        html.H4(str(mean_time_response_total)),
                    ],
                    className="kpi-card",
                ),
                html.Div(
                    [
                        html.H3("Median Time Response"),
                        html.H4(str(median_time_response_total)),
                    ],
                    className="kpi-card",
                ),
                # Ajouter le graphique de la jauge
                dcc.Graph(
                    id="gauge-discussions-closes",
                    figure=go.Figure(
                        go.Indicator(
                            mode="gauge+number",
                            value=discussions_closes,
                            title={"text": "Discussions Closes"},
                            domain={"x": [0, 1], "y": [0, 1]},
                            gauge={
                                "axis": {"range": [0, total_discussions], "tickwidth": 1, "tickcolor": "darkblue"},
                                "bar": {"color": "darkgreen"},
                                "bgcolor": "white",
                                "borderwidth": 2,
                                "bordercolor": "gray",
                                "steps": [{"range": [0, total_discussions], "color": "lightgray"}],
                                "threshold": {
                                    "line": {"color": "red", "width": 4},
                                    "thickness": 0.75,
                                    "value": discussions_closes,
                                },
                            },
                        )
                    ),
                    className="kpi-card",
                ),
            ],
            className="kpi-container",
        ),
        # ... (le reste de votre code)
    ]
)

# ... (le reste de votre code)

# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
