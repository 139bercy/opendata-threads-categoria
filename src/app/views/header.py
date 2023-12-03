from dash import html
import dash_bootstrap_components as dbc

# En-tête (header)
header = html.Div(
    [
        html.Img(src="static/assets/images/mefsin.svg", className="header-image"),
        html.H1("Tableau de bord d'analyse des discussions du MEFSIN", className="header-title"),
        dbc.Col(
            html.Button("Se connecter", id="login-button", className="btn btn-primary"),
            width="auto",  # La largeur "auto" utilise l'espace nécessaire pour le bouton
        ),
    ],
    className="header",
)