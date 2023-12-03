import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd 
import os

from flask import Flask, render_template, request, jsonify, make_response
from src.auth.infrastructure import InMemoryAccountRepository, PostgresqlAccountRepository

from src.auth.exceptions import LoginError, UsernameError
from src.auth.usecases import login as user_login

from src.app.views.sidebar import sidebar
from src.app.views.header import header
from src.app.views.graphs import filtres, treemap_fig, barchart, pie_chart, jauge_disc_closes, kpi 
from src.app.views import dashboard, formulaire, dataset

from dash.dependencies import Input, Output
import base64
from dash import callback_context

repository = PostgresqlAccountRepository()
if os.environ["APP_ENV"] == "test":
    repository = InMemoryAccountRepository()

# Initialiser le serveur Flask
server = Flask(__name__, template_folder="src/app/templates")
server.config["SECRET_KEY"] = "asma"
server.config["WTF_CSRF_ENABLED"] = False

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.MATERIA, dbc.icons.FONT_AWESOME],
    assets_folder="static", 
)

# Chargement des données depuis le fichier CSV (peut être placé dans app.py)
df = pd.read_csv("data/raw/inference/predicted_data_model2.csv")

app.layout = html.Div(
    [
        sidebar,
        dash.page_container,
        header,
        #dashboard_layout(),
        # Composant de gestion de l'URL
        dcc.Location(id="url", refresh=False),
        # Contenu de la page actuelle
        html.Div(id="page-content"),
    ], className="flex-container",
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

# Callback pour afficher le contenu de la vue en fonction de l'URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/" or pathname == "/accueil":
        return dashboard.dashboard_layout()
    elif pathname == "/form":
        # Appliquez le décorateur @login_required uniquement à la vue associée à '/form'
        return formulaire.layout()
    elif pathname == "/dataset":
        return dataset.dataset_layout()
    else:
        return "404 - Page introuvable"

if __name__ == "__main__":
    app.run_server(debug=True)