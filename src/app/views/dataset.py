import dash_html_components as html
from dash_table import DataTable
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import io
import base64
from dash import callback_context

# Charger le DataFrame
df = pd.read_csv("data/raw/inference/predicted_data_model2.csv")

def datasets_layout():
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


@app.callback(
    Output("download-link", "href"),
    [Input("table", "data")],
)
def update_download_link(data):
    if not callback_context.triggered_id:
        # Si la mise à jour n'est pas déclenchée par un événement de clic sur le bouton
        raise dash.exceptions.PreventUpdate

    # Convertir les données en DataFrame
    df_download = pd.DataFrame(data)

    # Convertir le DataFrame en CSV
    csv_string = df_download.to_csv(index=False, encoding="utf-8")

    # Convertir en base64 et créer le lien de téléchargement
    csv_base64 = base64.b64encode(csv_string.encode("utf-8")).decode("utf-8")
    href = f"data:text/csv;base64,{csv_base64}"

    return href
