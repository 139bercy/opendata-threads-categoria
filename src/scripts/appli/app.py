from flask import Flask, send_file
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import locale
import calendar
import io
import base64

# Importer les vues
from vues import vue1

# Configuration de l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/styles.css'])
server = Flask(__name__)  # Utiliser Flask en tant que serveur principal

# Charger les données depuis le fichier CSV
df = pd.read_csv('../../../data/raw/inference/predicted_data_model2.csv')

# Définir la fonction pour générer le contenu du fichier CSV
def generate_csv_data():
    csv_data = df.to_csv(index=False)
    csv_data_bytes = csv_data.encode('utf-8')
    return base64.b64encode(csv_data_bytes).decode('utf-8')

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
        # Vous pouvez ajouter d'autres vues ici si nécessaire
        return 'Contenu de la vue 2'
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

    csv_data_base64 = generate_csv_data()

    # Nom du fichier CSV pour le téléchargement
    file_name = 'predicted_data_model2.csv'

    # Message de téléchargement avec lien
    download_link = html.A('Télécharger le fichier', href=f'/download/{file_name}', download=file_name)

    return True, download_link, None

# Ajouter un endpoint Flask pour le téléchargement
@server.route('/download/<filename>')
def download_file(filename):
    csv_data_base64 = generate_csv_data()
    csv_data = base64.b64decode(csv_data_base64)
    return send_file(io.BytesIO(csv_data), mimetype='text/csv', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    server.run(debug=True)
