import dash_bootstrap_components as dbc
from dash import html, dcc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    soumettre = SubmitField("submit")


def layout():
    form = LoginForm()

    return dbc.Container(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Location(id="url", refresh=False),
                            html.Form(
                                method="post",
                                action="/api/v1/login",
                                children=[
                                    form.hidden_tag(),
                                    html.Div(
                                        [
                                            html.Label("Utilisateur"),
                                            dcc.Input(
                                                id="nom-input",
                                                type="text",
                                                name="username",
                                                className="form-control",
                                            ),
                                        ],
                                        className="form-group",
                                    ),
                                    html.Br(),
                                    html.Div(
                                        [
                                            html.Label("Mot de passe"),
                                            dcc.Input(
                                                id="prenom-input",
                                                type="text",
                                                name="password",
                                                className="form-control",
                                            ),
                                        ],
                                        className="form-group",
                                    ),
                                    html.Br(),
                                    html.Button(
                                        "Se connecter",
                                        type="submit",
                                        className="btn btn-primary",
                                    ),
                                ],
                            ),
                        ],
                        width=6,
                    ),
                ],
                className="mt-4",
            ),
        ],
        fluid=True,
    )
