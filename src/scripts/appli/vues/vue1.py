# Import des bibliothèques nécessaires
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.express as px
import pandas as pd
import locale
from app import app  # Importez l'objet app depuis app.py
import calendar

# Configuration de la localisation en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Obtention des noms des mois en français
mois_en_francais = list(calendar.month_name)[1:]

# Chargement des données depuis le fichier CSV (peut être placé dans app.py)
df = pd.read_csv('../../../data/raw/inference/predicted_data_model2.csv')

# Définition de la mise en page de la vue1
def layout():
    # Création d'une division pour les filtres, le calendrier et la chronologie
    filters_div = html.Div([
        # Filtre interactif pour la catégorie (labels)
        html.Label('Filtrer par catégorie :'),
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': label, 'value': label} for label in df['predictions_motifs_label'].unique()],
            multi=True  # Permet de sélectionner plusieurs catégories
        ),

        # Sélecteur de plage de dates de style calendrier
        html.Label('Sélectionnez une plage de dates :'),
        dcc.DatePickerRange(
            id='date-range-picker',
            start_date=df['created_discussion'].min(),
            end_date=df['created_discussion'].max(),
            display_format='DD/MM/YYYY'  # Format de date français
        ),

        # Curseur de chronologie
        dcc.RangeSlider(
            id='timeline-filter',
            min=0,
            max=len(mois_en_francais) - 1,
            step=1,
            marks={i: mois_en_francais[i] for i in range(len(mois_en_francais))},
            value=[0, len(mois_en_francais) - 1]  # Valeur par défaut (toute la période)
        ),

        # Conteneur HTML personnalisé pour afficher les mois en français
        html.Div(id='selected-months-output', style={'margin-top': 10}),
    ], className='sticky-filters')  # Ajouter la classe CSS 'sticky-filters'

    # Création d'une fonction pour générer la treemap en fonction des données filtrées
    def generate_treemap(filtered_data):
        fig = px.treemap(
            filtered_data, 
            path=['predictions_motifs_label', 'predictions_ssmotifs_label'], 
            width=1800, 
            height=700
        )

        # Personnalisation du texte de la légende
        labels = {
            'predictions_motifs_label': 'Label des motifs',
            'predictions_ssmotifs_label': 'Label des sous-motifs'
        }

        # Centrer la légende
        title_font = {'size': 30, 'color': 'black', 'family': 'Arial'}

        fig.update_traces(textinfo="label+value",
                          textposition='middle center',  # Centrer le texte horizontalement et verticalement
                          insidetextfont={'size': 20},  # Définir la taille de la police du texte à 20
                          hovertemplate='')  # Désactiver les info-bulles

        fig.update_layout(margin=dict(t=80, l=0, r=10, b=10))
        fig.update_layout(title="Mosaïque des discussions : Visualisation de l'importance des problèmes rencontrés par catégorie",
                          title_font=title_font)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig.update_traces(textfont_size=10, selector=dict(type='treemap'))

        return fig

    # Utilisation de cette fonction pour créer la figure initiale
    treemap_fig = generate_treemap(df)

    # Création d'une fonction pour générer le sunburst en fonction des données filtrées
    def generate_sunburst(filtered_data):
        fig = px.sunburst(
            filtered_data,
            path=['predictions_motifs_label', 'predictions_ssmotifs_label'],
            width=1650,
            height=600
        )

        # Personnalisation du texte de la légende
        labels = {
            'predictions_motifs_label': 'Label des motifs',
            'predictions_ssmotifs_label': 'Label des sous-motifs'
        }

        # Centrer la légende
        title_font = {'size': 30, 'color': 'black', 'family': 'Arial'}

        fig.update_traces(textinfo="label+value",
                          insidetextfont={'size': 20},  # Définir la taille de la police du texte à 20
                          hovertemplate='')  # Désactiver les info-bulles

        fig.update_layout(margin=dict(t=80, l=0, r=10, b=10))
        fig.update_layout(title="Visualisation de l'importance des problèmes rencontrés par jeux de données",
                          title_font=title_font)

        return fig

    # Ajouter un nouvel élément Div pour le deuxième graphique (sunburst)
    sunburst_div = html.Div([
        html.Hr(),  # Ajouter une ligne horizontale pour séparer les graphiques
        dcc.Graph(id='sunburst-graph', figure=generate_sunburst(df))  # Ajouter le graphique sunburst
    ])

    return html.Div([
        # Ajout de la division des filtres au-dessus de votre graphique
        filters_div,
        
        # Graphique de la treemap
        dcc.Graph(id='treemap-graph', figure=treemap_fig),

        # Ajouter le graphique sunburst
        sunburst_div
    ])

# Callback function pour mettre à jour le graphique sunburst
@app.callback(
    Output('sunburst-graph', 'figure'),
    [Input('filter-selector', 'value'),
     Input('category-filter', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('timeline-filter', 'value')]
)
def update_sunburst_chart(filter_selector, selected_categories, start_date, end_date, timeline_value):
    try:
        # Convertir les dates en objets DateTime si ce n'est pas déjà le cas
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        if filter_selector == 'calendar':
            # Filtre basé sur le calendrier
            filtered_df = df[(df['predictions_motifs_label'].isin(selected_categories)) &
                             (df['created_discussion'] >= start_date) &
                             (df['created_discussion'] <= end_date)]

        elif filter_selector == 'timeline':
            # Filtre basé sur la chronologie
            start_month_index, end_month_index = timeline_value
            selected_start_month = pd.Timestamp(f"{start_month_index + 1}/1/{start_date.year}")
            selected_end_month = pd.Timestamp(f"{end_month_index + 1}/1/{end_date.year}")

            filtered_df = df[(df['predictions_motifs_label'].isin(selected_categories)) &
                             (df['created_discussion'] >= selected_start_month) &
                             (df['created_discussion'] <= selected_end_month)]

        # Utiliser la fonction pour générer le graphique sunburst
        updated_sunburst_fig = generate_sunburst(filtered_df)

        return updated_sunburst_fig
    except Exception as e:
        print(str(e))  # Afficher l'erreur dans la console pour le débogage
