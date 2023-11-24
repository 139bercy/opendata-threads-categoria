from flask import Flask, render_template, request
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from dash import dcc

# from flask_login import LoginManager, login_required, login_user, logout_user, current_user
# from auth import Utilisateur, LoginForm, InscriptionForm
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

# from auth.auth import app as auth_app  # Importez l'application d'authentification
from src.app.vues import vue1, vue2

# Importer la fonction de mise en page depuis vue1


# Ajoutez le chemin du dossier auth au chemin de recherche du système
# auth_path = Path(__file__).resolve().parents[2]  # Remplacez le nombre selon la structure de vos dossiers
# sys.path.append(str(auth_path))

# Initialiser le serveur Flask
server = Flask(__name__)
server.config["SECRET_KEY"] = "asma"
server.config["WTF_CSRF_ENABLED"] = False  # Désactiver le jeton CSRF

"""server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utilisateurs.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
login_manager = LoginManager(server)
login_manager.login_view = 'login'"""

# Initialiser l'application Dash avec Bootstrap
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configurez la page de connexion pour être affichée si un utilisateur non authentifié tente d'accéder à une page protégée
# login_manager.login_view = 'login'

# En-tête de l'application
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

# Intégrer le fichier CSS
app.external_stylesheets = [dbc.themes.BOOTSTRAP, "static/assets/style.css"]

"""
@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(nom=form.nom.data, prenom=form.prenom.data).first()
        if utilisateur and check_password_hash(utilisateur.mot_de_passe, form.mot_de_passe.data):
            login_user(utilisateur)
            flash('Connexion réussie.', 'success')
            return redirect(url_for('accueil'))
        else:
            flash('Échec de la connexion. Veuillez vérifier vos informations.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accueil'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    if form.validate_on_submit():
        if form.mot_de_passe.data == form.confirmer_mot_de_passe.data:
            mot_de_passe_hashe = generate_password_hash(form.mot_de_passe.data, method='sha256')
            nouvel_utilisateur = Utilisateur(nom=form.nom.data, prenom=form.prenom.data, mot_de_passe=mot_de_passe_hashe)
            db.session.add(nouvel_utilisateur)
            db.session.commit()
            flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Les mots de passe ne correspondent pas.', 'danger')
    return render_template('inscription.html', form=form)

@app.route('/accueil')
@login_required
def accueil():
    return f'Page d\'accueil. Bonjour, {current_user.prenom} {current_user.nom}!'

"""


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
