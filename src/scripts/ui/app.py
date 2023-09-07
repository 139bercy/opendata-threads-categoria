# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import date
import locale

# Définir la locale française pour le formatage de la date
locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')

# Incorporate data
df = pd.read_csv('data/discussions-annotations-public-.csv')
#print(df.columns)


# Initialize the app - incorporate a Dash Bootstrap theme
#LITERA, LUMEN, MATERIA, QUARTZ, SANDSTONE, SPACELAB
external_stylesheets = [dbc.themes.MATERIA]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            # Logo à gauche avec une marge à droite de 3 (espacement personnalisé)
            dbc.Col(html.Img(src='/assets/logo_ministere.png', height="40px"), width="auto", className="mx-auto"),
            # Titre au milieu avec une marge horizontale de 5 (espacement personnalisé)
            dbc.Col(dbc.NavbarBrand("Tableau de Bord des discussions du MEFSIN"), width="auto", align="center", className="mx-auto"),
            # Lien à droite avec une marge à gauche de 3 (espacement personnalisé)
            dbc.Col(dbc.NavItem(dbc.NavLink("Site de data.economie.gouv.fr", href="https://data.economie.gouv.fr/pages/accueil/")), width="auto", align="end", className="mx-auto")
        ],
        align="center"),
    ]),
    color="primary",
    dark=True,
    className="mb-100",  # Marge en bas (espacement personnalisé)
    sticky="top"  # Pour rendre la barre de navigation fixe en haut
)

# Add the Count column
df['Count'] = df.shape[0]

# Group by category and subcategory
grouped_df = df.groupby(['categorie', 'Annotation'])

# Calculate the distribution of discussions by category and subcategory
category_counts = grouped_df['Count'].sum().reset_index()

# Sort the categories by count in descending order
category_counts = category_counts.sort_values('Count', ascending=False)

# Define custom colors for each category
category_colors = {
    'Premiere categorie': 'blue',
    'Seconde categorie': 'orange',
    'Troisieme categorie': 'green',
    'Quatrieme categorie': 'purple',
    'Cinquieme categorie': 'yellow',
    'Sixieme categorie': 'cyan'
}

# Create the treemap chart using Plotly Express
treemap_fig = px.treemap(category_counts,
                         path=['categorie', 'Annotation'],
                         values='Count',
                         color='Count',
                         #color='categorie',
                         #color_discrete_map=category_colors)
                         color_continuous_scale='Blues')

# Update the layout of the graph to change the figure size
treemap_fig.update_layout(
    width=1600,   # Specify the width in pixels
    height=700,   # Specify the height in pixels
    #paper_bgcolor='white',  # Set the background color to white
    #plot_bgcolor='white'    # Set the background color of the whole plot to white
)

# Update the text properties of the labels in the treemap
treemap_fig.update_traces(textinfo='label+value+percent parent',
                          textposition='middle center',
                          hoverinfo='label+value+percent parent',
                          hovertemplate='<b>%{label}</b><br>%{value}<br>%{percentParent}',
                          hoverlabel=dict(bgcolor='white', font_size=16),
                          insidetextfont=dict(size=16))

# App layout
app.layout = dbc.Container([
    # Barre de navigation
    navbar, 
    
    dbc.Row([
        html.H1('Tableau de Bord des discussions du MEFSIN', className="text-primary text-center fs-1")
    ]),
    
    dbc.Tabs([
        dbc.Tab(label='Dashboard 1', children=[
            html.Br(),
            html.H2("Aperçu du jeu de données des discussions"),
            html.Br(),
            # Ajouter le contenu spécifique au Dashboard 1 ici
            dbc.Row([
            dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                        value='lifeExp',
                        inline=True,
                        id='radio-buttons-final')
            ]),
            html.Br(),
            dbc.Row([
                dcc.DatePickerRange(id='date-picker-range',
                                    #start_date=date(1997, 5, 3),
                                    start_date=date.today(),  # Format jour/mois/année
                                    end_date_placeholder_text='Sélectionnez une date !',
                                    display_format='DD/MM/YYYY')  # Format d'affichage
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_table={'overflowX': 'auto'})
                ], width=12),
            ]),
            html.P("Ce dataframe répertorie l'ensemble des discussions tournant autour des jeux de données du MEFSIN. Le but de cette étude est de permettre aux métiers de mieux comprendre les problèmes rencontrés par les utilisateurs qui utilisent leurs jeux de données publiés sur la plateforme."),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='my-first-graph-final')
                ], width=6),
                
                dbc.Col([
                    dcc.Graph(figure={}, id='my-second-graph-final')
                ], width=6),
            ]),
        ]),
        
        dbc.Tab(label='Dashboard 2', children=[
            html.H2("Dashboard 2 Content"),
            # Ajouter le contenu spécifique au Dashboard 2 ici
            html.Br(),
            html.H2("Distribution des discussions par catégorie et sous-catégories"),
            # CATEGORIES
            dcc.Graph(figure=treemap_fig, id='category-distribution-treemap'),
            #dcc.Graph(figure=treemap_fig, id='category-distribution-treemap', style={'background-color': 'white'}),
            # SOUS-CATEGORIES
        ]),
        
        dbc.Tab(label='Dashboard 3', children=[
            html.H2("Dashboard 3 Content"),
            # Ajouter le contenu spécifique au Dashboard 3 ici
        ]),
    ]),  
], fluid=True)

# Add controls to build the interaction
"""@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig
    """
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8051)
