import calendar
import locale

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import des bibliothèques nécessaires
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Configuration de la localisation en français
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

# Obtention des noms des mois en français
mois_en_francais = list(calendar.month_name)[1:]

# Chargement des données depuis le fichier CSV (peut être placé dans app.py)
df = pd.read_csv("data/raw/inference/predicted_data_model2.csv")

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

############################################"FILTRES"##########################################################

# Création d'une division pour les filtres, le calendrier et la chronologie
filtres = html.Div(
    [
        html.Label("Filtrer par catégorie :"),  # Filtre interactif pour la catégorie (labels)
        dcc.Dropdown(
            id="category-filter",
            options=[{"label": label, "value": label} for label in df["predictions_motifs_label"].unique()],
            multi=True,
        ),
        html.Label("Sélectionnez une plage de dates :"),  # Sélecteur de plage de dates de style calendrier
        dcc.DatePickerRange(
            id="date-range-picker",
            start_date=df["created_discussion"].min(),
            end_date=df["created_discussion"].max(),
            display_format="DD/MM/YYYY",
        ),
        dcc.RangeSlider(
            id="timeline-filter",
            min=0,
            max=len(mois_en_francais) - 1,
            step=1,
            marks={i: mois_en_francais[i] for i in range(len(mois_en_francais))},
            value=[0, len(mois_en_francais) - 1],
        ),
        html.Div(id="selected-months-output", style={"margin-top": 10}),
    ],
    className="sticky-filters",
)
############################################"GRAPHS"##########################################################
# TREEMAP

# Fonction pour générer la treemap en fonction des données filtrées
def generate_treemap(filtered_data):
    fig = px.treemap(
        filtered_data,
        path=["predictions_motifs_label", "predictions_ssmotifs_label"],
        width=None,  # Définir la largeur à None pour permettre la responsivité
        height=620,  # Définir la hauteur à None pour permettre la responsivité
    )

    # Personnalisation du texte de la légende
    labels = {
        "predictions_motifs_label": "Label des motifs",
        "predictions_ssmotifs_label": "Label des sous-motifs",
    }

    fig.update_traces(
        textinfo="label+value",
        textposition="middle center",
        insidetextfont={"size": 20},
        hovertemplate="",
    )

    fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    fig.update_layout(
        title_text="Mosaïque des discussions : Visualisation de l'importance des problèmes rencontrés par catégorie",
        title_font=dict(color="black", size=18),
        title_x=0.5,  # centre le titre horizontalement
        title_y=0.987,
    )

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_traces(textfont_size=15, selector=dict(type="treemap"))

    return dcc.Graph(figure=fig)

# Utilisation de cette fonction pour créer la figure initiale
treemap_fig = generate_treemap(df)

# BARCHART

# Fonction pour générer le graphique en barres des JDD les plus discutés
def generate_bar_chart(jdd_counts):
    return dcc.Graph(
        id="bar-chart-jdd-discutes",
        figure=px.bar(
            y=jdd_counts.index,
            x=jdd_counts.values,
            orientation="h",
            title="JDD les plus discutés",
            category_orders={"y": list(jdd_counts.index)},
            text=jdd_counts.values,
            labels={"x": "Nombre de Discussions", "y": "Slug jdd"},
            height=800,
            width=None,
        ),
    )

# Utilisation de cette fonction pour créer le graphique en barres
barchart = generate_bar_chart(jdd_counts)

# PIECHART

# Fonction pour générer le graphique circulaire (pie chart) pour la proportion de discussions ouvertes et fermées
pie_chart = dcc.Graph(
                id="pie-chart-discussions",
                figure=px.pie(
                    names=["Discussions Ouvertes", "Discussions Closes"],
                    values=[discussions_ouvertes, discussions_closes],
                    #title="Proportion de Discussions Ouvertes et Closes",
                    color_discrete_sequence=["#ED4646", "#33BB5C"],
                    hole=0.4,
                ).update_traces(
                    texttemplate="<b>%{percent:.0%}</b>",
                    insidetextfont=dict(size=16),
                ),
            )

# JAUGE DISCUSSIONS CLAUSES
jauge_disc_closes = dcc.Graph(
                            id="jauge-discussions-closes",
                            figure=go.Figure(
                                go.Indicator(
                                    mode="gauge+number",
                                    value=discussions_closes,
                                    title={"text": "Nombre de discussions Closes"},
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
                            ))

# Ajout des KPIs
kpi = html.Div(
    [
        html.H3("Statistiques de la plateforme :", className="title-kpi"),
        html.Div([
            dbc.Card(
                [
                    dbc.CardHeader("Total discussions"),
                    dbc.CardBody(
                        [
                            html.H4(total_discussions, className="card-title1")
                        ]
                    ),
                ],
                style={"width": "12rem"},
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Discussions ouvertes"),
                    dbc.CardBody(
                        [
                            html.H4(discussions_ouvertes, className="card-title1")
                        ]
                    ),
                ],
                style={"width": "12rem"},
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Temps de réponses moyen"),
                    dbc.CardBody(
                        [
                            html.H4(str(mean_time_response_total), className="card-title2")
                        ]
                    ),
                ],
                style={"width": "12rem"},
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Temps de réponses médian"),
                    dbc.CardBody(
                        [
                            html.H4(str(median_time_response_total), className="card-title3")
                        ]
                    ),
                ],
                style={"width": "12rem"},
            ),
            ], className="kpi-cards-container",
        )
    ], className="kpi-container",
)