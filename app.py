import base64
import os
import sys

import dash
import dash_bootstrap_components as dbc
import flask
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask, render_template, request, make_response, jsonify

from src.app.views import formulaire, dataset
from src.app.views import sidebar, header, dashboard
from src.app.views.auth import login
from src.app.views.graphs import treemap_fig
from src.auth.exceptions import InvalidToken
from src.auth.exceptions import LoginError, UsernameError
from src.auth.infrastructure import PostgresqlAccountRepository, InMemoryAccountRepository
from src.auth.usecases import login as user_login, check_token, decode_token

# Importez FlaskForm du module wtforms
from flask_wtf import FlaskForm
# Importez TextAreaField pour traiter le champ de texte du formulaire
from wtforms import StringField, SubmitField, TextAreaField

# Ajoutez le chemin du projet au chemin d'import
#project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
#sys.path.append(project_path)

from src.scripts.inference import inference_script
from src.app.views import sandbox

# Initialiser le serveur Flask
server = Flask(__name__, template_folder="src/app/templates")
server.config["SECRET_KEY"] = "asma"
server.config["WTF_CSRF_ENABLED"] = False

repository = PostgresqlAccountRepository()
if os.environ["APP_ENV"] == "test":
    repository = InMemoryAccountRepository()

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.MATERIA, dbc.icons.FONT_AWESOME],
    assets_folder="static",
)
# pour le formulaire flask !
app.config['suppress_callback_exceptions'] = True

# Chargement des données depuis le fichier CSV (peut être placé dans app.py)
df = pd.read_csv("data/raw/inference/predicted_data_models.csv")

app.layout = html.Div(
    [
        sidebar.layout,
        dash.page_container,
        header.layout,
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ],
    className="flex-container",
)


# Callback function pour mettre à jour le graphique sunburst
@app.callback(
    Output("treemap-graph", "figure"),
    [
        Input("category-filter", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
        Input("timeline-filter", "value"),
    ],
)
def update_charts(selected_categories, start_date, end_date, timeline_value):
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        start_month_index, end_month_index = timeline_value
        selected_start_month = pd.Timestamp(f"{start_month_index + 1}/1/{start_date.year}")
        selected_end_month = pd.Timestamp(f"{end_month_index + 1}/1/{end_date.year}")

        filtered_df = df[
            (df["predictions_motifs_label"].isin(selected_categories))
            & (df["created_discussion"] >= start_date)
            & (df["created_discussion"] <= end_date)
            & (df["created_discussion"].dt.month >= start_month_index + 1)
            & (df["created_discussion"].dt.month <= end_month_index + 1)
        ]

        updated_treemap_fig = treemap_fig

        return updated_treemap_fig
    except Exception as e:
        print(str(e))


# Routes
@server.route("/form_traite", methods=["POST"])
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

# Définir le callback pour mettre à jour le lien de téléchargement
@app.callback(
    Output("download-link", "href"),
    [Input("download-link", "n_clicks")],
)
def update_download_link(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    df_download = df
    # Convertir le DataFrame en CSV
    csv_string = df_download.to_csv(index=False, encoding="utf-8")

    # Convertir en base64 et créer le lien de téléchargement
    csv_base64 = base64.b64encode(csv_string.encode("utf-8")).decode("utf-8")
    href = f"data:text/csv;base64,{csv_base64}"

    return href


@app.callback(Output("login-error", "children"), [Input("url", "pathname")], [State("url", "search")])
def display_error(pathname, search):
    if search:
        error_message = search.split("=")[1]
        return dbc.Alert(f"Error: {error_message}", color="danger")
    return None


@app.callback(
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("username-input", "value"),
    State("password-input", "value"),
)
def check_login(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate
    try:
        session_token = user_login(repository=repository, username=username, password=password)
        token = str(session_token)
        dash.callback_context.response.set_cookie("session-token", token) #envoie le cookies au navigateur pour le stocker en mémoire
        return dcc.Location(pathname="/", id="homepage")
    except (LoginError, UsernameError, KeyError) as e:
        print(e)
        return dbc.Alert("Mauvais couple d'identifiants.", color="warning", dismissable=True)
    except TypeError:
        pass


@server.route("/test/user-is-logged-in", methods=["GET"])
def user_is_logged_in():
    cookies = flask.request.cookies
    user_session_cookie = cookies.get("session-token", "No cookie found")
    try:
        is_logged = check_token(repository=repository, encoded_token=user_session_cookie)
        username, token = decode_token(user_session_cookie)
        return make_response(
            jsonify({"username": username, "token": token, "cookie": user_session_cookie, "is logged in": is_logged}),
            200,
        )
    except Exception as e:
        return make_response(jsonify(f"Error: {e}"), 403)


def login_required(repository, view_func):
    cookies = flask.request.cookies
    try:
        user_session_cookie = cookies.get("session-token", None)
        if not user_session_cookie:
            return dcc.Location(href="/login", id="login-page")
        user_is_logged_in = check_token(repository=repository, encoded_token=user_session_cookie)
        if not user_is_logged_in:
            return dcc.Location(href="/login", id="login-page")
        return view_func
    except InvalidToken:
        return dcc.Location(href="/login", id="login-page")


# Callback pour gérer le clic sur le bouton de connexion/déconnexion
@app.callback(
    [
        Output("login-logout-icon", "className"),
        Output("login-logout-text", "children"),
        Output("login-logout-link", "href"),
    ],
    [Input("login-logout-link", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_login_logout(n_clicks):
    print("Toggle Clicks:", n_clicks)

    # Obtenir le cookie de session
    cookies = flask.request.cookies
    user_session_cookie = cookies.get("session-token", None)
    print("Session Cookie:", user_session_cookie)

    if user_session_cookie:
        # L'utilisateur est connecté donc bouton deconnexion
        dash.callback_context.response.delete_cookie("session-token") #envoie le cookies au navigateur pour le stocker en mémoire
        #return "fa fa-sign-out", "Se déconnecter", "/"
        return "fa fa-sign-out", "", "/"
    
    # L'utilisateur n'est pas connecté, donc connexion
    #return "fa fa-sign-in", "Se connecter", "/login"
    return "fa fa-sign-in", "", "/login"


# Ajoutez la route pour le formulaire
@server.route("/form", methods=["GET", "POST"])
def sandbox_route():
    return sandbox.sandbox()

# Ajoutez une nouvelle route pour le résultat du formulaire
@server.route("/form/result", methods=["POST"])
def process_form():
    title = request.form.get("title")
    message = request.form.get("message")
    return sandbox.process_form(title, message)

# Callback pour afficher le contenu de la vue en fonction de l'URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/" or pathname == "/home":
        return login_required(repository, dashboard.dashboard_layout())
    elif pathname == "/login":
        return login.layout
    #elif pathname == "/form":
        #Appliquez le décorateur @login_required uniquement à la vue associée à '/form'
        #return login_required(repository, formulaire.layout())
    elif pathname == "/dataset":
        return dataset.dataset_layout()
    elif pathname == "/form":
        return sandbox.sandbox()
    elif pathname == "/form/result":
        return sandbox.process_form()
    else:
        return "404 - Page introuvable"


if __name__ == "__main__":
    app.run_server(debug=True)
