import dash_bootstrap_components as dbc
from dash import dcc, html

def create_dropdown(options, label='', id=''):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(html.Label(label),style={'text-align' : 'right'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(options, options[0], searchable=False, clearable=False, id=id)
            ], width=12)
        ])
    ], fluid=True)

def create_radioitems(label='', id=''):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(html.Label(label),style={'text-align' : 'right'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.RadioItems(id=id)
            ], width=4)
        ], justify='end')
    ], fluid=True)
