import dash_html_components as html
from dash_table import DataTable
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import io


# Charger le DataFrame
df = pd.read_csv("data/raw/inference/predicted_data_model2.csv")

def dataset_layout():
    return html.Div(
        [
            html.H2("Présentation du jeu de données", style={"color": "white"}),

            # Afficher le tableau
            DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in df.columns],
                data=df.to_dict('records'),
                style_table={'height': '300px', 'overflowY': 'auto'},
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
                    ),
                ],
                className="mt-3",
            ),
        ],
        className="dataset",
    )

