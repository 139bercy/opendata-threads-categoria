from src.app.views.header import header
from dash import html, dcc
from .graphs import filtres, treemap_fig, barchart, pie_chart, jauge_disc_closes, kpi, barchart_views, barchart_reuses

def dashboard_layout():
    return html.Div(
        [
            html.Div(
                [
                    html.Hr(),
                    filtres,
                    html.Hr(),
                    html.Div(
                        [
                            html.Div(
                                [
                                    treemap_fig,
                                ],
                                className="treemap-container"
                            ),
                            html.Div(
                                [
                                    barchart,
                                ],
                                className="barchart-container"
                            ),
                            html.Div(
                                [
                                    html.H3("Proportion des discussions ouvertes / closes :", className="status-title"),
                                    html.Div([
                                        pie_chart,
                                        jauge_disc_closes,
                                        ], className="status-container"
                                    ),
                                ],
                            ),
                            html.Div(
                                [
                                    kpi,
                                ],
                                className="kpi-container"
                            ),
                            html.Div(
                                [
                                    barchart_views,
                                    barchart_reuses,
                                ],
                                className="tendances-container"
                            ),
                        ], 
                        className="graphs-container"
                    )
                ],
                className="dashboard-container",
            ),
        ],
    )
