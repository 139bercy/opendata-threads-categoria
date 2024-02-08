from dash import html, dcc
from .graphs import (
    filtres,
    treemap_fig,
    barchart,
    pie_chart,
    jauge_disc_closes,
    kpi,
    bar_chart_top_jdd_views,
    bar_chart_top_jdd_reuses,
    second_treemap_fig
)


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
                                className="treemap-container",
                            ),
                            html.Div(
                                [
                                    # barchart,
                                    dcc.Graph(figure=barchart, id="barchart"),
                                ],
                                className="barchart-container",
                            ),
                            html.Div(
                                [
                                    html.H3("Proportion des discussions ouvertes / closes :", className="status-title"),
                                    html.Div(
                                        [
                                            pie_chart,
                                            jauge_disc_closes,
                                        ],
                                        className="status-container",
                                    ),
                                ],
                            ),
                            html.Div(
                                [
                                    kpi,
                                ],
                                className="kpi-container",
                            ),
                            html.Div(
                                [
                                    # barchart_views,
                                    # barchart_reuses,
                                    dcc.Graph(figure=bar_chart_top_jdd_views, id="bar_chart_top_jdd_views"),
                                    dcc.Graph(figure=bar_chart_top_jdd_reuses, id="bar_chart_top_jdd_reuses"),
                                    # graph_row,
                                ],
                                className="tendances-container",
                            ),
                            # Ajouter le deuxième treemap
                            html.Div([second_treemap_fig], className="second-treemap-container"),
                        ],
                        className="graphs-container",
                    ),
                ],
                className="dashboard-container",
            ),
        ],
    )
