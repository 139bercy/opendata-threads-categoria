import dash_bootstrap_components as dbc
from dash import html

sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("CategorIA", style={"color": "white"}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fa fa-chart-simple me-3"), html.Span("Dashboard")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        # html.I(className="fa fa-commenting me-2"),
                        html.I(className="fa fa-gamepad me-3", style={"margin-left": "-3px"}),
                        html.Span("Jouer avec l'IA"),
                    ],
                    href="/form",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-database me-3"),
                        html.Span("Dataset"),
                    ],
                    href="/dataset",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-github me-3"),
                        html.Span("GitHub"),
                    ],
                    href="https://github.com/AsmaRACHIDI/Projet_Discussions.git",
                    target="_blank",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)
