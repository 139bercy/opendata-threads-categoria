import os

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask import Flask, render_template, request, jsonify, make_response

from src.app.vues import vue1, vue2
from src.auth.exceptions import LoginError, UsernameError
from src.auth.infrastructure import InMemoryAccountRepository, PostgresqlAccountRepository
from src.auth.usecases import login as user_login

repository = PostgresqlAccountRepository()
if os.environ["APP_ENV"] == "test":
    repository = InMemoryAccountRepository()

# Initialiser le serveur Flask
server = Flask(__name__, template_folder="src/app/templates")
server.config["SECRET_KEY"] = "asma"
server.config["WTF_CSRF_ENABLED"] = False

app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.external_stylesheets = [dbc.themes.BOOTSTRAP, "static/assets/style.css"]

header = html.Div(
    [
        # Logo de l'entreprise ou de l'application (colonne 1)
        html.Div(
            [
                html.Img(
                    src="static/assets/images/mefsin.svg",
                    style={
                        "height": "230px",
                        "width": "230px",
                        "margin-top": "-50px",
                        "margin-bottom": "-30px",
                    },
                )
            ],
            className="col-lg-2 col-md-4 col-sm-4 col-12 text-right",
        ),
        # Titre de l'application (colonne 2)
        html.Div(
            [
                html.H1(
                    "Tableau de bord d'analyse des discussions du MEFSIN",
                    id="header-title",
                    style={"margin-top": "40px"},
                )
            ],
            className="col-lg-8 col-md-4 col-sm-4 col-12 text-center",
        ),
        # Bouton de téléchargement du jeu de données (colonne 3)
        html.Div(
            [
                dcc.ConfirmDialogProvider(
                    children=[
                        html.Button(
                            "Télécharger les données",
                            id="download-button",
                            className="btn btn-primary",
                            style={"margin-top": "35px", "padding": "15px"},
                        )
                    ],
                    id="download-data-confirm",
                    message="Êtes-vous sûr de vouloir télécharger les données ?",
                )
            ],
            className="col-lg-2 col-md-4 col-sm-4 col-12 text-center",
        ),
    ],
    className="header row",
)

# Mise en page principale de l'application Dash
app.layout = html.Div(
    [
        header,
        # Composant de gestion de l'URL
        dcc.Location(id="url", refresh=False),
        # Contenu de la page actuelle
        html.Div(id="page-content"),
    ],
    style={"margin": "20px"},
)


# Routes


@app.server.route("/form_traite", methods=["POST"])
def traiter_formulaire():
    if request.method == "POST":
        # Récupérer les valeurs du formulaire
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")

        # Faites quelque chose avec les données (par exemple, les imprimer)
        print(f"Nom: {nom}, Prénom: {prenom}")

        # Ajoutez le code pour enregistrer les données dans la base de données
        # et pour alimenter le modèle d'IA avec ces données

        # Redirigez l'utilisateur vers une nouvelle page ou faites autre chose selon vos besoins
        return render_template("formulaire_traite.html", nom=nom, prenom=prenom)


@app.server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form.to_dict()
        try:
            session_token = user_login(repository=repository, username=data["username"], password=data["password"])
            token = str(session_token)
            response = make_response(jsonify({"message": "Login successful", "token": str(token)}), 200)
            response.set_cookie("token", token)
            return response
        except (LoginError, UsernameError, KeyError):
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html", error=None)


# Callback pour afficher le contenu de la vue en fonction de l'URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/" or pathname == "/accueil":
        return vue1.layout()
    elif pathname == "/form":
        # Appliquez le décorateur @login_required uniquement à la vue associée à '/form'
        return vue2.layout()
    else:
        return "404 - Page introuvable"


# Exécuter le serveur Flask
if __name__ == "__main__":
    server.run(debug=True)
