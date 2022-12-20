import dash_bootstrap_components as dbc
from dash import dcc, html

def create_graph(label_id='', graph_id=''):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4(id=label_id, style={'text-align' : 'center'})
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
                html.H5(id=top_metric_id, style={'text-align' : 'center'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('R2 Score', style={'text-align' : 'right'})
            ], width=6, align='center'),
            dbc.Col([
                html.H6(id=middle_metric_id, style={'text-align' : 'left'})
            ], width=6, align='center')
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Direction match', style={'text-align' : 'right'})
            ], width=6, align='center'),
            dbc.Col([
                html.H6(id=bottom_metric_id, style={'text-align' : 'left'})
            ], width=6, align='center')
        ]) 
    ], fluid=True)

#     dbc.Row([
#         dbc.Col([
#             html.Div(dbc.Container([
#                 dbc.Row([
#                     dbc.Col([
#                         html.Br(),
#                         html.H5(id='stock-code-name', style={'text-align' : 'center'})
#                     ], width=12, align='center')
#                 ]),
#                 dbc.Row([
#                     dbc.Col([
#                         html.Br(),
#                         html.H6(id='r2-metric-label', children='R2 Score', style={'text-align' : 'right'}),
#                         html.Br()
#                     ], width=6, align='center'),
#                     dbc.Col([
#                         html.Br(),
#                         html.H5(id='r2-metric', style={'text-align' : 'left'}),
#                         html.Br()
#                     ], width=6, align='center'),
#                 ]),
#                 dbc.Row([
#                     dbc.Col([
#                         html.H6(children='Direction match', style={'text-align' : 'right'}),
#                         html.Br()
#                     ], width=6, align='center'),
#                     dbc.Col([
#                         html.H5(id='direction-accuracy-metric', style={'text-align' : 'left'}),
#                         html.Br()
#                     ], width=6, align='center'),
#                 ]),
#             ]), style={'border-top' : '1px grey dotted'})
#         ], width=6),  
#     ]),    
# ], fluid=True)





    #     dbc.Row([
    #     dbc.Col([
    #         html.H4(id='line-chart-actuals-label', style={'text-align' : 'center'})
    #     ], width=6),
    #     dbc.Col([
    #         html.H4(id='line-chart-prediction-label', style={'text-align' : 'center'})
    #     ], width=6),
    # ]),    
    # dbc.Row([
    #     dbc.Col([
    #         html.Div(dcc.Graph(id='line-chart-actuals'), style={'border' : '1px grey dotted'})
    #     ], width=6),
    #     dbc.Col([
    #         html.Div(dcc.Graph(id='line-chart-prediction'), style={'border' : '1px grey dotted'})
    #     ], width=6),        
    # ]),
    # dbc.Row([
    #     dbc.Col([
    #         html.Br()
    #     ], width=12),
    # ]),   