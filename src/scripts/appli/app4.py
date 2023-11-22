from flask import Flask, render_template, request
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from dash import dcc

from vues import vue1, vue2

# Initialiser le serveur Flask
server = Flask(__name__)
server.config['SECRET_KEY'] = 'asma'
server.config['WTF_CSRF_ENABLED'] = False # Désactiver le jeton CSRF


# Initialiser l'application Dash avec Bootstrap
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Tableau de bord d'analyse des discussions du MEFSIN", className="ml-2"),
        ],
        fluid=True,
    ),
)

# Mise en page principale de l'application Dash
app.layout = html.Div([
    # Navbar
    navbar,
    
    # Composant de gestion de l'URL
    dcc.Location(id='url', refresh=False),
    
    # Contenu de la page actuelle
    html.Div(id='page-content'),
])

@app.server.route('/form_traite', methods=['POST'])
def traiter_formulaire():
    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')

        # Faites quelque chose avec les données (par exemple, les imprimer)
        print(f'Nom: {nom}, Prénom: {prenom}')

        # Ajoutez le code pour enregistrer les données dans la base de données
        # et pour alimenter le modèle d'IA avec ces données

        # Redirigez l'utilisateur vers une nouvelle page ou faites autre chose selon vos besoins
        return render_template('formulaire_traite.html', nom=nom, prenom=prenom)

# Callback pour afficher le contenu de la vue en fonction de l'URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/' or pathname == '/accueil':
        return vue1.layout()  # Appel de la mise en page de vue1
    elif pathname == '/form':
        return vue2.layout()  # Appel de la mise en page de vue2
    else:
        return '404 - Page introuvable'

# Exécuter le serveur Flask
if __name__ == "__main__":
    server.run(debug=True)
