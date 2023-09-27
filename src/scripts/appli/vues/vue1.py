from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import locale
# Import the object app from app.py
from app import app
import calendar

# Set the locale configuration to French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Get the names of months in French
mois_en_francais = list(calendar.month_name)[1:]

# Load data from the CSV file (can be placed in app.py)
df = pd.read_csv('../../../data/raw/inference/predicted_data_model2.csv')

# Ajoutez la div pour les filtres, le calendrier et la timeline comme indiqué précédemment
filters_div = html.Div([
    # Interactive filter for category (labels)
    html.Label('Filtrer par catégorie :'),
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': label, 'value': label} for label in df['predictions_motifs_label'].unique()],
        multi=True  # Allows selecting multiple categories
    ),

    # Calendar-style date range picker
    html.Label('Sélectionnez une plage de dates :'),
    dcc.DatePickerRange(
        id='date-range-picker',
        start_date=df['created_discussion'].min(),
        end_date=df['created_discussion'].max(),
        display_format='DD/MM/YYYY'  # French date format
    ),

    # Filter timeline slider
    dcc.RangeSlider(
        id='timeline-filter',
        min=0,
        max=len(mois_en_francais) - 1,
        step=1,
        marks={i: mois_en_francais[i] for i in range(len(mois_en_francais))},
        value=[0, len(mois_en_francais) - 1]  # Default value (all time)
    ),

    # Custom HTML container to display months in French
    html.Div(id='selected-months-output', style={'margin-top': 10}),
], className='sticky-filters')  # Ajoutez la classe CSS 'sticky-filters'

# Créez une fonction pour générer la treemap en fonction des données filtrées
#def generate_treemap(filtered_data):
    #return px.treemap(filtered_data, path=['predictions_motifs_label', 'predictions_ssmotifs_label'], width=1813, height=700)

def generate_treemap(filtered_data):
    fig = px.treemap(
        filtered_data, 
        path=['predictions_motifs_label', 'predictions_ssmotifs_label'], 
        width=1800, 
        height=700
    )

    # Personnalisez le texte de la légende
    labels = {
        'predictions_motifs_label': 'Label des motifs',
        'predictions_ssmotifs_label': 'Label des sous-motifs'
    }

    # Centrez la légende
    title_font = {'size': 30, 'color': 'black', 'family': 'Arial'}

    fig.update_traces(textinfo="label+value",
                      textposition='middle center',  # Centre le texte horizontalement et verticalement
                      insidetextfont={'size': 20},  # Définit la taille de la police du texte à 20
                      hovertemplate='')  # Désactiver les bulles d'info (tooltips)
    
    fig.update_layout(margin=dict(t=10, l=0, r=10, b=10))
    fig.update_layout(title="Mosaïque des discussions : Visualisation de l'importance des problèmes rencontrés par catégorie",
                      title_font=title_font)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_traces(textfont_size=20, selector=dict(type='treemap'))

    return fig


# Utilisez cette fonction pour créer la figure initiale
fig = generate_treemap(df)

# Define the layout
def layout():
    return html.Div([
        # Ajoutez la div des filtres au-dessus de votre graphique
        filters_div,
        
        # Treemap chart
        dcc.Graph(id='graph-1', figure=fig)
    ])

# Callback to update the chart based on the selected filter
@app.callback(
    [Output('selected-months-output', 'children'),
     Output('graph-1', 'figure')],
    [Input('filter-selector', 'value'),
     Input('category-filter', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('timeline-filter', 'value')]
)
def update_graph(filter_selector, selected_categories, start_date, end_date, timeline_value):
    try:
        # Convert dates to DateTime objects if they are not already
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        if filter_selector == 'calendar':
            # Calendar-based filter
            filtered_df = df[(df['predictions_motifs_label'].isin(selected_categories)) &
                             (df['created_discussion'] >= start_date) &
                             (df['created_discussion'] <= end_date)]

            # Translate months to French
            selected_months = pd.date_range(start_date, end_date, freq='MS').strftime('%B %Y')
            months_in_french = [mois_en_francais[int(month.split()[0])] + ' ' + month.split()[1] for month in selected_months]

        elif filter_selector == 'timeline':
            # Timeline-based filter
            start_month_index, end_month_index = timeline_value
            selected_start_month = pd.Timestamp(f"{start_month_index + 1}/1/{start_date.year}")
            selected_end_month = pd.Timestamp(f"{end_month_index + 1}/1/{end_date.year}")

            filtered_df = df[(df['predictions_motifs_label'].isin(selected_categories)) &
                             (df['created_discussion'] >= selected_start_month) &
                             (df['created_discussion'] <= selected_end_month)]

            # Translate months to French
            selected_months = pd.date_range(selected_start_month, selected_end_month, freq='MS').strftime('%B %Y')
            months_in_french = [mois_en_francais[int(month.split()[0])] + ' ' + month.split()[1] for month in selected_months]

        # Display months as HTML text
        months_html = ', '.join(months_in_french)

        updated_fig = generate_treemap(filtered_df)
        
        return months_html, updated_fig
    except Exception as e:
        print(str(e))  # Display the error in the console for debugging
