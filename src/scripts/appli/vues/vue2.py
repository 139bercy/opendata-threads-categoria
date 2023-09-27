from dash import html
from dash import dcc
import pandas as pd

# Chargez les données depuis le fichier CSV
df = pd.read_csv('../../../data/raw/inference/predicted_data_model2.csv')

def layout():
    return html.Div([
        html.H1('Vue 2'),
        dcc.Graph(id='graph-2'),
        # Ajoutez d'autres composants spécifiques à cette vue
    ])
