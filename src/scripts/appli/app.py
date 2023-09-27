import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html, dcc
import plotly.express as px
import pandas as pd
# Importer les vues
from vues import vue1, vue2  # Importez les fichiers de vue
import locale
import calendar
import io
import base64
from dash.exceptions import PreventUpdate

# Définir la configuration locale en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Charger les données depuis le fichier CSV
df = pd.read_csv('../../../data/raw/inference/predicted_data_model2.csv')

# Configuration de l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/styles.css'])
server = app.server

# Mise en page principale de l'application
app.layout = html.Div([
    # En-tête de l'application
    html.Div([
        # Logo de l'entreprise ou de l'application (colonne 1)
        html.Div([
            html.Img(src='/assets/images/mefsin.svg', style={'height': '250px', 'width': '250px', 'margin-top': '-50px', 'margin-bottom': '-50px'})
        ], className='col-lg-2 col-md-4 col-sm-4 col-12 text-right'),

        # Titre de l'application (colonne 2)
        html.Div([
            html.H1("Tableau de bord d'analyse des discussions du MEFSIN", style={'margin-top': '40px'})
        ], className='col-lg-8 col-md-4 col-sm-4 col-12 text-center'),

        # Bouton de téléchargement du jeu de données (colonne 3)
        html.Div([
            dcc.ConfirmDialogProvider(
                children=[
                    html.Button('Télécharger les données', id='download-button', className='btn btn-primary', style={'margin-top': '35px', 'padding': '15px'})
                ],
                id='download-data-confirm',
                message='Êtes-vous sûr de vouloir télécharger les données ?'
            )
        ], className='col-lg-2 col-md-4 col-sm-4 col-12 text-center'),
    ], className='header row'),

    # Contenu de la page actuelle
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], style={'margin': '20px'})

# Définir les routes pour chaque vue
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return vue1.layout()  # Appel de la mise en page de vue1
    elif pathname == '/vue2':
        return vue2.layout()  # Appel de la mise en page de vue2
    else:
        return '404 - Page introuvable'

# Définir la fonction de callback globale pour gérer le téléchargement des données
@app.callback(
    Output('download-data-confirm', 'displayed'),
    Output('download-data-confirm', 'message'),
    Output('download-button', 'n_clicks'),
    [Input('download-data-confirm', 'submit_n_clicks')]
)
def download_data(submit_n_clicks):
    if not submit_n_clicks:
        raise PreventUpdate

    # Générer le contenu du fichier CSV (à adapter à votre besoin)
    csv_data = df.to_csv(index=False)

    # Convertissez les données CSV en bytes
    csv_data_bytes = csv_data.encode('utf-8')

    # Créez un objet io.BytesIO à partir des données
    csv_data_io = io.BytesIO(csv_data_bytes)

    # Encodez les données en base64 pour le téléchargement
    csv_data_base64 = base64.b64encode(csv_data_io.read()).decode('utf-8')

    # Nom du fichier CSV pour le téléchargement
    file_name = '../../../data/raw/inference/predicted_data_model2.csv'

    # Message de téléchargement avec lien
    download_link = html.A('Télécharger le fichier', href=f'data:text/csv;charset=utf-8;base64,{csv_data_base64}', download=file_name)

    return True, download_link, None

if __name__ == '__main__':
    app.run_server(debug=True)
