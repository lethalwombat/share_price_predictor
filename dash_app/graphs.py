import dash_bootstrap_components as dbc
from dash import dcc, html

def create_graph(label_id='', graph_id=''):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5(id=label_id, style={'text-align' : 'center'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(
                    dcc.Graph(id=graph_id),
                style={'border' : '1px grey dotted'})
            ], width=12)
        ])
    ], fluid=True)

def create_metrics_widget(top_metric_id='', middle_metric_id='', bottom_metric_id=''):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5()
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(style={'border-top' : '1px grey dotted'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([html.Br()
            ], width=12)
        ]),       
        dbc.Row([
            dbc.Col([
                html.H5(id=top_metric_id, style={'text-align' : 'center'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H6('R2 Score', style={'text-align' : 'right'})
            ], width=6, align='center'),
            dbc.Col([
                html.H5(id=middle_metric_id, style={'text-align' : 'left'})
            ], width=6, align='center')
        ]),
        dbc.Row([
            dbc.Col([
                html.H6('Direction match', style={'text-align' : 'right'})
            ], width=6, align='center'),
            dbc.Col([
                html.H5(id=bottom_metric_id, style={'text-align' : 'left'})
            ], width=6, align='center')
        ]) 
    ], fluid=True)
