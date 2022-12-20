import sys
sys.path.append('/helpers')
from engine import run_model
import pandas as pd

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px
from stock_codes import stock_codes
from model_input_selectors import create_dropdown, create_radioitems
from graphs import create_graph, create_metrics_widget

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
app.title = 'Stock Price Predictor'

server = app.server

# selector values
stock_codes_values = sorted([k['name'].upper() for k in stock_codes])

# object wrap
graph_wrap = lambda obj, width : dbc.Col([obj], width=width)
graphs = dbc.Container([
    dbc.Row([
        graph_wrap(create_graph(label_id='line-chart-actuals-label', graph_id='line-chart-actuals'), 6),
        graph_wrap(create_graph(label_id='line-chart-prediction-label', graph_id='line-chart-prediction'), 6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Br()
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            create_metrics_widget(top_metric_id='stock-code-name', middle_metric_id='r2-metric', bottom_metric_id='direction-accuracy-metric')
        ], width=6),
        dbc.Col([
            create_graph(label_id='bar-chart-prediction-label', graph_id='bar-chart-prediction')
        ], width=6),        
    ]),
], fluid=True)

dropdown_definitions = [
    create_dropdown(stock_codes_values, 'Select stock code:', id='dropdown-stock-code'),
    create_dropdown([str(i) for i in range(2010, 2020)], 'Last year of training data:', id='dropdown-year'),
    create_dropdown([i for i in range(1, 4)], 'Training data years:', id='dropdown-data-size'),
    create_radioitems(['  0.01', '  0.05', '  0.1', '  0.15'], 'Learning rate:', id='input-learning-rate'),
    create_dropdown([50, 100, 150], 'Number of estimators:', id='input-dropdown-estimators')
]

# wrap each drop down in row and col
dropdown_wrap = lambda obj : dbc.Row([dbc.Col([obj], width=12)])

dropdowns = dbc.Container([
    dropdown_wrap(create_dropdown(stock_codes_values, 'Select stock code:', id='dropdown-stock-code')),
    dropdown_wrap(create_dropdown([str(i) for i in range(2010, 2020)], 'Last year of training data:', id='dropdown-year')),
    dropdown_wrap(create_dropdown([i for i in range(1, 4)], 'Training data years:', id='dropdown-data-size')),
    dropdown_wrap(create_radioitems(['  0.01', '  0.05', '  0.1', '  0.15'], 'Learning rate:', id='input-learning-rate')),
    dropdown_wrap(create_dropdown([50, 100, 150], 'Number of estimators:', id='input-dropdown-estimators')) 
], fluid=True)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H4('Model inputs', style={'text-align' : 'center'}),
            html.Br()
        ], width=2, align='end'),
        dbc.Col([
            html.Br(),
            html.H2('Stock Price Predictor', style={'text-align' : 'center', 'font-weight' : 'bold'}),
            html.Br(),
        ], width=10)
    ]),
    dbc.Row([
        dbc.Col([
            dropdowns
        ], width=2, align='start'),
        dbc.Col([
            graphs
        ], width=10, align='start')
    ])
], fluid=True)


@app.callback(
    [
        Output('line-chart-actuals', 'figure'),
        Output('line-chart-prediction', 'figure'),
        Output('bar-chart-prediction', 'figure'),
        Output('line-chart-actuals-label', 'children'),
        Output('line-chart-prediction-label', 'children'),
        Output('stock-code-name', 'children'),        
        Output('r2-metric', 'children'),
        Output('direction-accuracy-metric', 'children')
    ],
    [
        Input('dropdown-stock-code', 'value'),
        Input('dropdown-year', 'value'),
        Input('dropdown-data-size', 'value'),
        Input('input-learning-rate', 'value'),
        Input('input-dropdown-estimators', 'value')
    ])
def update_graph(value, value_year, value_size, value_learning_rate, value_n_estimators):
    df = (
        run_model(value, value_year, training_data_size=value_size, learning_rate=float(value_learning_rate.strip()), n_estimators=value_n_estimators)
        .rename(columns={
            'price_next_day' : 'Actual', 
            'price_next_day_simulated' : 'Prediction',
            'date' : 'Date',
            'actual' : 'Actual growth',
            'prediction' : 'Predicted growth'
            })
    )
    # calculate growth direction match
    df = (
        df
        .assign(direction_match=df.\
                apply(lambda row : 'green' if \
                    ((row['Actual growth'] > 0) & (row['Predicted growth'] > 0)) |\
                    ((row['Actual growth'] < 0) & (row['Predicted growth'] < 0))\
                    else 'red', axis=1))
        .rename(columns={'direction_match' : 'Direction'})
    )
    # set up charts
    line_chart_actuals = (
    px.line(
        df.query('subset=="training"'),
        x='Date',
        y=['Actual', 'Prediction'],
        labels={
            'value' : 'Price'
        },
        color_discrete_map={
            'Actual' : '#1f77b4',
            'Prediction' : '#d62728'
        }
        )
        .update_layout({
        'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
        'paper_bgcolor' : 'rgba(0, 0, 0, 0)'},
        legend_title='', hovermode='x unified')
        .update_traces(mode='lines', hovertemplate='%{y:$.2f}<extra></extra>')
    )
    line_chart_prediction = (
    px.line(
        df.query('subset=="validation"'),
        x='Date',
        y=['Actual', 'Prediction'],
        labels={
            'value' : 'Price'
        },
        color_discrete_map={
            'Actual' : '#1f77b4',
            'Prediction' : '#d62728'
        }
        )
        .update_layout({
        'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
        'paper_bgcolor' : 'rgba(0, 0, 0, 0)'},
        legend_title='', hovermode='x unified')
        .update_traces(mode='lines', hovertemplate='%{y:$.2f}<extra></extra>')
        .update_xaxes(rangeslider_visible=True)
    )
    bar_chart_prediction = (
        px.bar(
            (df
            .query('subset=="validation"')
            ),
            x='Date',
            y='Predicted growth'
        )
        .update_layout({
        'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
        'paper_bgcolor' : 'rgba(0, 0, 0, 0)'}, hovermode=False, yaxis_tickformat='.0%')
        .update_traces(marker_color=df.query('subset=="validation"')['Direction'])
    )
    # calculate metrics
    stock_code_name = [s['description'] for s in stock_codes if s['name'] == value][0]
    r2_score = '{:.1%}'.format(df['r2_train'].unique()[0])
    direction_accuracy = '{:.1%}'\
        .format(df.query('subset == "validation" & Direction == "green"').shape[0] / df.query('subset == "validation"').shape[0])    

    # generate chart titles
    chart_titles = [
        f'Model fit for {value} using {value_size} years of data from {int(value_year)-value_size+1} to {value_year}',
        f'Model prediction for {value} stock price movement in {int(value_year) + 1}'
    ]
    if value_size == 1:
        chart_titles = [c.replace('years', 'year') for c in chart_titles]
    return line_chart_actuals, line_chart_prediction, bar_chart_prediction, chart_titles[0], chart_titles[1], stock_code_name, r2_score, direction_accuracy


# development
if __name__ == '__main__':
    app.run_server(port='8050', host='0.0.0.0', debug=True)
