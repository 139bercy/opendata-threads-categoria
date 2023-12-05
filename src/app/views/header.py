from dash import html
import dash_bootstrap_components as dbc

# En-tête (header)
layout = html.Div(
    [
        dbc.NavLink(html.Img(src="static/assets/images/mefsin.svg", className="header-image"), href="/"),
        html.H1("Tableau de bord d'analyse des discussions du MEFSIN", className="header-title"),
        dbc.Col(
            dbc.Button("Me connecter", id="login-button", href="/login"),
            width="auto",  # La largeur "auto" utilise l'espace nécessaire pour le bouton
        ),
    ],
    className="header",
)
