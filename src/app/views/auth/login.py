import dash_bootstrap_components as dbc
from dash import html, dcc

layout = dbc.Container(
    html.Div(
        [
            html.H1("Login", style={"text-align": "center"}),
            html.Label("Identifiant:", style={"margin-top": "10px", "font-weight": "bold"}),
            dcc.Input(id="username-input", type="text", value="", style={"width": "100%", "margin-bottom": "10px"}),
            html.Label("Mot de passe:", style={"margin-top": "10px", "font-weight": "bold"}),
            dcc.Input(id="password-input", type="password", value="", style={"width": "100%", "margin-bottom": "10px"}),
            html.Button(
                "Me connecter",
                id="login-button",
                n_clicks=0,
                style={
                    "background-color": "#4CAF50",
                    "color": "white",
                    "padding": "10px 15px",
                    "border": "none",
                    "cursor": "pointer",
                },
            ),
            html.Div(id="login-output", style={"margin-top": "20px", "font-weight": "bold"}),
        ]
    )
)
