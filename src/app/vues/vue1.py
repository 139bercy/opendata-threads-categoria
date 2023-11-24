# vue1.py

# Import des bibliothèques nécessaires
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import locale
from src.app.app import app
import calendar

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
jdd_reuses = (
    df.groupby("title_dataset")["nb_reuses"].first().sort_values(ascending=False)
)

# Calculer les JDD les plus consultés
jdd_views = df.groupby("title_dataset")["nb_views"].first().sort_values(ascending=False)

# Calculer les JDD avec le plus de followers
jdd_followers = (
    df.groupby("title_dataset")["nb_followers"].first().sort_values(ascending=False)
)

# Calculer le nombre de discussions ouvertes et fermées
discussions_closes = pd.to_datetime(
    df["closed_discussion"], format="%d/%m/%Y", errors="coerce"
).count()
discussions_ouvertes = total_rows - discussions_closes

# Calcul du temps de réponse d'un commentaire entre l'ouverture de la discussion et sa fermeture
df["created"] = pd.to_datetime(
    df["created_discussion"], format="%d/%m/%Y", errors="coerce"
)
df["closed"] = pd.to_datetime(
    df["closed_discussion"], format="%d/%m/%Y", errors="coerce"
)
df["time_response"] = df["closed"] - df["created"]

# Calculer la moyenne des temps de réponse par annotation
mean_time_response = (
    df.groupby("title_discussion")["time_response"].mean().sort_values(ascending=False)
)

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

    fig.update_traces(
        textinfo="label+value", insidetextfont={"size": 20}, hovertemplate=""
    )

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
            html.Label(
                "Filtrer par catégorie :"
            ),  # Filtre interactif pour la catégorie (labels)
            dcc.Dropdown(
                id="category-filter",
                options=[
                    {"label": label, "value": label}
                    for label in df["predictions_motifs_label"].unique()
                ],
                multi=True,
            ),
            html.Label(
                "Sélectionnez une plage de dates :"
            ),  # Sélecteur de plage de dates de style calendrier
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
    sunburst_div = html.Div(
        [html.Hr(), dcc.Graph(id="sunburst-graph", figure=generate_sunburst(df))]
    )

    bar_chart_div = generate_bar_chart(jdd_counts)

    pie_chart_div = generate_pie_chart(discussions_ouvertes, discussions_closes)

    return html.Div(
        [
            filters_div,  # Ajout de la division des filtres au-dessus de votre graphique
            dcc.Graph(
                id="treemap-graph", figure=treemap_fig, className="responsive-graph"
            ),  # Graphique de la treemap
            sunburst_div,
            bar_chart_div,
            pie_chart_div,
        ]
    )


# Callback function pour mettre à jour le graphique sunburst
@app.callback(
    Output("sunburst-graph", "figure"),
    [
        Input("category-filter", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
        Input("timeline-filter", "value"),
    ],
)
def update_sunburst_chart(selected_categories, start_date, end_date, timeline_value):
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        start_month_index, end_month_index = timeline_value
        selected_start_month = pd.Timestamp(
            f"{start_month_index + 1}/1/{start_date.year}"
        )
        selected_end_month = pd.Timestamp(f"{end_month_index + 1}/1/{end_date.year}")

        filtered_df = df[
            (df["predictions_motifs_label"].isin(selected_categories))
            & (df["created_discussion"] >= start_date)
            & (df["created_discussion"] <= end_date)
            & (df["created_discussion"].dt.month >= start_month_index + 1)
            & (df["created_discussion"].dt.month <= end_month_index + 1)
        ]

        updated_sunburst_fig = generate_sunburst(filtered_df)

        return updated_sunburst_fig
    except Exception as e:
        print(str(e))


# Exemple de mise à jour de l'app.layout
# app.layout = layout
