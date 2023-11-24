from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class MonFormulaire(FlaskForm):
    nom = StringField('Nom')
    prenom = StringField('Prénom')
    soumettre = SubmitField('Soumettre')

def layout():
    form = MonFormulaire()

    return dbc.Container(
        [
            dbc.Row(dbc.Col(html.H1("Formulaire"), width=12)),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Location(id='url', refresh=False),
                            html.Form(
                                method='post',
                                action='/traiter_formulaire',
                                children=[
                                    form.hidden_tag(),
                                    html.Div(
                                        [
                                            html.Label('Nom'),
                                            dcc.Input(id='nom-input', type='text', name='nom', className='form-control'),
                                        ],
                                        className='form-group',
                                    ),
                                    html.Div(
                                        [
                                            html.Label('Prénom'),
                                            dcc.Input(id='prenom-input', type='text', name='prenom', className='form-control'),
                                        ],
                                        className='form-group',
                                    ),
                                    
                                    html.Button('Soumettre', type='submit', className='btn btn-primary'),
                                ],
                            ),
                        ],
                        width=6,
                    ),
                ],
                className='mt-4',
            ),
        ],
        fluid=True,
    )