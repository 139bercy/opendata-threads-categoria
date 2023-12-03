# vue1.py

import calendar
import locale

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import des bibliothèques nécessaires
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#from src.app.app import app

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


# Fonction pour générer la treemap en fonction des données filtrées
def generate_treemap(filtered_data):
    fig = px.treemap(
        filtered_data,
        path=["predictions_motifs_label", "predictions_ssmotifs_label"],
        width=None,  # Définir la largeur à None pour permettre la responsivité
        height=630,  # Définir la hauteur à None pour permettre la responsivité
    )

    # Personnalisation du texte de la légende
    labels = {
        "predictions_motifs_label": "Label des motifs",
        "predictions_ssmotifs_label": "Label des sous-motifs",
    }

    # Centrer la légende
    title_font = {"size": 30, "color": "black", "family": "Arial"}

    fig.update_traces(
        textinfo="label+value",
        textposition="middle center",
        insidetextfont={"size": 20},
        hovertemplate="",
    )

    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    fig.update_layout(
        title="Mosaïque des discussions : Visualisation de l'importance des problèmes rencontrés par catégorie",
        title_font=title_font,
        title_x=0.5,
        title_y=0.96,
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_traces(textfont_size=15, selector=dict(type="treemap"))

    return fig


# Fonction pour générer le sunburst en fonction des données filtrées
def generate_sunburst(filtered_data):
    fig = px.sunburst(
        filtered_data,
        path=["predictions_motifs_label", "predictions_ssmotifs_label"],
        width=None,
        height=None,
    )

    # Personnalisation du texte de la légende
    labels = {
        "predictions_motifs_label": "Label des motifs",
        "predictions_ssmotifs_label": "Label des sous-motifs",
    }

    # Centrer la légende
    title_font = {"size": 30, "color": "black", "family": "Arial"}

    fig.update_traces(textinfo="label+value", insidetextfont={"size": 20}, hovertemplate="")

    fig.update_layout(margin=dict(t=80, l=0, r=10, b=10))
    fig.update_layout(
        title="Visualisation de l'importance des problèmes rencontrés par jeux de données",
        title_font=title_font,
    )

    return fig


# Fonction pour générer le graphique en barres des JDD les plus discutés
def generate_bar_chart(jdd_counts):
    return html.Div(
        [
            html.Hr(),
            dcc.Graph(
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
                    width=1860,
                ),
            ),
        ]
    )


# Fonction pour générer le graphique circulaire (pie chart) pour la proportion de discussions ouvertes et fermées
def generate_pie_chart(discussions_ouvertes, discussions_closes):
    return html.Div(
        [
            html.Hr(),
            dcc.Graph(
                id="pie-chart-discussions",
                figure=px.pie(
                    names=["Discussions Ouvertes", "Discussions Closes"],
                    values=[discussions_ouvertes, discussions_closes],
                    title="Proportion de Discussions Ouvertes et Closes",
                    color_discrete_sequence=["#ED4646", "#33BB5C"],
                    hole=0.4,
                ).update_traces(
                    texttemplate="<b>%{percent:.0%}</b>",
                    insidetextfont=dict(size=16),
                ),
            ),
        ]
    )


# Fonction pour créer la mise en page de vue1
def layout():
    # Création d'une division pour les filtres, le calendrier et la chronologie
    filters_div = html.Div(
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

    # Utilisation de cette fonction pour créer la figure initiale
    treemap_fig = generate_treemap(df)

    # Ajouter un nouvel élément Div pour le deuxième graphique (sunburst)
    sunburst_div = html.Div([html.Hr(), dcc.Graph(id="sunburst-graph", figure=generate_sunburst(df))])

    bar_chart_div = generate_bar_chart(jdd_counts)

    pie_chart_div = generate_pie_chart(discussions_ouvertes, discussions_closes)

    # Ajout des KPIs
    kpi_div = html.Div(
        [
            html.Div(
                [
                    html.H3("Total Discussions", className="card-title"),
                    html.H4(total_discussions, className="card-text"),
                ],
                className="card kpi-card",
            ),
            html.Div(
                [
                    html.H3("Open Discussions"),
                    html.H4(discussions_ouvertes),
                ],
                className="kpi-card",
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Marketing"),
                    dbc.CardBody(
                        [
                            html.H4("201 new Leads", className="card-title"),
                            html.P("Delivered this week compared...", className="card-text"),
                        ]
                    ),
                ],
                style={"width": "30rem"},
            ),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("Card title", className="card-title"),
                            html.P(
                                "$10.5 M",
                                className="card-value",
                            ),
                        ]
                    )
                ]
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
            )])
    
    # Ajouter le graphique de la jauge
    jauge_disc_closes = dcc.Graph(
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
                            ))
    
    """
        # Ajout des KPIs
    kpi_div2 = html.Div([
                    html.Div(
                        [
                            #html.H6("Total Discussions", className="card-title"),
                            #html.H4(total_discussions, className="card-text"),
                            html.H6(children='Total des discussions',
                                    style={
                                        'textAlign': 'center',
                                        'color': 'black'}
                                    ),
                            
                            html.P(total_discussions,
                                   style={
                                       'textAlign': 'center',
                                        'color': 'black',
                                        'fontSize': 40}
                                   )
                        ],
                        className="card_container three columns"),
                    
                    html.Div(
                        [
                            html.H6(children='Discussions non-fermées',
                                    style={
                                        'textAlign': 'center',
                                        'color': 'black'}
                                    ),
                            
                            html.P(discussions_ouvertes,
                                   style={
                                       'textAlign': 'center',
                                        'color': 'Black',
                                        'fontSize': 40}
                                   )
                        ],
                        className="card_container three columns"),
                    
                    html.Div(
                        [
                            html.H6(children='Temps de réponse moyen',
                                    style={
                                        'textAlign': 'center',
                                        'color': 'black'}
                                    ),
                            
                            html.P(mean_time_response_total,
                                   style={
                                       'textAlign': 'center',
                                        'color': 'Black',
                                        'fontSize': 40}
                                   )
                        ],
                        className="card_container three columns"),
                    
                    html.Div(
                        [
                            html.H6(children='Temps de réponse médian',
                                    style={
                                        'textAlign': 'center',
                                        'color': 'black'}
                                    ),
                            
                            html.P(median_time_response_total,
                                   style={
                                       'textAlign': 'center',
                                        'color': 'Black',
                                        'fontSize': 40}
                                   )
                        ],
                        className="card_container three columns")
                    ], className="row flex-display"),

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
        className="kpi-card")"""
    
    

    return html.Div(
        [
            filters_div,  # Ajout de la division des filtres au-dessus de votre graphique
            dcc.Graph(id="treemap-graph", figure=treemap_fig, className="responsive-graph"),  # Graphique de la treemap
            sunburst_div,
            bar_chart_div,
            pie_chart_div,
            kpi_div,
            jauge_disc_closes,
        ]
    )




# Exemple de mise à jour de l'app.layout
# app.layout = layout
