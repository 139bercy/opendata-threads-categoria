from dash import html
from dash.dash_table import DataTable
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import io


# Charger le DataFrame
df = pd.read_csv("data/raw/inference/predicted_data_models.csv")

# Réinitialiser l'index du DataFrame
df = df.reset_index()

def dataset_layout():
    return html.Div(
        [
            html.H3("Présentation du jeu de données annoté par le modèle d'IA", className="title-dataset"),
            # Afficher le tableau
            DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in df.columns],
                data=df.to_dict('records'),
                style_table={'height': '630px', 'width': None, 'overflowY': 'auto'},
                style_cell={'textAlign': 'left', 'minWidth': '50px'},
                page_size=20,  # Définir le nombre d'éléments par page
                style_header={'backgroundColor': '#293e57', 'color': 'white'},
                style_data={'backgroundColor': '#d6d6d642'},
                style_data_conditional=[
                    {
                        'if': {'state': 'selected'},
                        'backgroundColor': '#293e5740',
                        'border': '1px solid white'
                    }
                ],
            ),

            # Ajouter le bouton de téléchargement
            html.Div(
                [
                    html.A(
                        "Télécharger le jeu de données",
                        id="download-link",
                        download="dataset.csv",
                        href="",
                        target="_blank",
                        className="btn btn-primary",
                        n_clicks=0  # Pour éviter le callback initial au chargement de la page
                    ),
                ],
                className="mt-3",
            ),
        ],
        className="dataset",
    )

