# Import des bibliothèques nécessaires
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

# Chargement des données depuis le fichier CSV
df = pd.read_csv('../../../data/raw/inference/predicted_data_model2.csv')

# Création de l'application Dash
app = Dash(__name__)

# Graphique en barres
bar_chart = dcc.Graph(
    id='bar-chart',
    figure=px.bar(
        df,
        x='predictions_motifs_label',
        title='Fréquence des motifs prédits',
        labels={'predictions_motifs_label': 'Motifs', 'count': 'Fréquence'}
    )
)

# Graphique en nuage de points
# Count occurrences of each combination
counts = df.groupby(['predictions_motifs_label', 'predictions_ssmotifs_label']).size().reset_index(name='count')

# Scatter plot
fig = px.scatter(
    counts,
    x='predictions_motifs_label',
    y='predictions_ssmotifs_label',
    size='count',
    title='Scatter Plot with Size Based on Count'
)
# Mise en page de l'application Dash
app.layout = html.Div([bar_chart, fig])

# Exécutez l'application
if __name__ == '__main__':
    app.run_server(debug=True)
