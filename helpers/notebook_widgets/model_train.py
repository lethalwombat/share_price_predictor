import sys
sys.path.append('/helpers')
import pandas as pd
from os import listdir
from itertools import product
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from ipywidgets import Dropdown, Button, Output
from IPython.display import clear_output
from dataframes import df_reshape


# widget options
_feature_files = sorted([f.split(".csv")[0] for f in listdir('/data') if f[0:8] == 'features'])

# set up notebook selectors
selectors = {
    'file' : {
        'description' : 'File:',
        'options' : _feature_files,
        'type' : Dropdown
    }
}

# set up widget default values
for s in selectors:
    selector_value = selectors[s]['options'][0]
    # set up the widget for display
    selectors[s]['display'] = selectors[s]['type'](
        description=selectors[s]['description'],
        options=selectors[s]['options'],
        value=selector_value
    )

def train_model(*args):
    with model_train_button_output:
        clear_output()
        # import the selected file
        selected_file = selectors['file']['display'].value
        features = pd.read_csv(f'/data/{selected_file}.csv', parse_dates=['Date'])
        print('Imported {:,} feature records\n'.format(features.shape[0]))
        # dataframe columns to be used as features
        selected_features = [
            'highest_5', 'highest_10', 'highest_30', 'highest_ever', 
            'is_monday', 'is_friday', 
            'increase_streak', 'decline_streak',
            'previous_swing',
            'rolling_2', 'rolling_3', 'rolling_5', 'rolling_7'
        ]
        # dataframe column to be use as target
        selected_target = 'adj_close_next_day'
        # fit the model for each stock code in the file
        reg = GradientBoostingRegressor()
        predictions = []
        for stock_code in features['stock_code'].unique():
            print(f'Fitting for {stock_code}')
            X_train = (
                features
                .query('subset=="training"')
                .query(f'stock_code=="{stock_code}"')
                [selected_features]
            )
            y_train = (
                features
                .query('subset=="training"')
                .query(f'stock_code=="{stock_code}"')
                [selected_target]
            )
            X_test = (
                features
                .query('subset=="validation"')
                .query(f'stock_code=="{stock_code}"')
                [selected_features]
            )
            y_test = (
                features
                .query('subset=="validation"')
                .query(f'stock_code=="{stock_code}"')
                [selected_target]
            )
            # fit the model and write predictions into the dataframes
            reg.fit(X_train, y_train)
            y_predicted_train, y_predicted_test = reg.predict(X_train), reg.predict(X_test)
            X_train['adj_close_prediction'], X_test['adj_close_prediction'] = y_predicted_train, y_predicted_test

            # add predictions
            predictions.append(X_train.copy()), predictions.append(X_test.copy())

        # add predictions to the input features file
        features = (
            pd.concat(predictions)
            [['adj_close_prediction']]
            .merge(features, how='right', left_index=True, right_index=True)
            .drop(columns=selected_features)
        )
        # add predictions to the downloaded data
        download = (
            pd.read_csv('/data/' + selected_file.replace('features', 'download') + '.csv', parse_dates=['Date'])
            .reset_index(drop=True)
            .merge(features, how='left', left_on=['Date', 'stock_code', 'subset'], right_on=['Date', 'stock_code', 'subset'])
        )
        # calculate actual and predicted prices for next day
        download['price_next_day'] = download['Adj Close'] * download['adj_close_next_day']
        download['price_next_day_predicted'] = download['Adj Close'] * download['adj_close_prediction']

        # calculate if the direction of the prediction matches, i.e. increase or decline
        download['direction_match'] = download.apply(\
            lambda row : 1 if any(
                [
                    ((row['adj_close_prediction'] > 1) & (row['adj_close_next_day'] > 1)),
                    ((row['adj_close_prediction'] < 1) & (row['adj_close_next_day'] < 1)),
                ]
            ) else 0, axis=1)

        # prepare the data for output
        dashboard_df = (
            download
            [['Date', 'stock_code', 'subset', 'Adj Close', 'price_next_day', 'price_next_day_predicted', 'direction_match']]
            .rename(columns={'Adj Close' : 'price_today'})
            .pipe(df_reshape)
        )
        # display accuracy stats
        metrics_df = {
            'stock_code' : [],
            'subset' : [],
            'r2' : [],
            'direction_accuracy' : []
            }
        print('\nModel accuracy metrics\n')
        for subset in product(dashboard_df['stock_code'].unique(), dashboard_df['subset'].unique()):
            metrics_df['stock_code'].append(subset[0]), metrics_df['subset'].append(subset[1])
            df_accuracy_stats = (
                dashboard_df
                .query('stock_code=="{}"'.format(subset[0]))
                .query('subset=="{}"'.format(subset[1]))
                [['price_next_day', 'price_next_day_predicted', 'direction_match']]
            )
            r2 = r2_score(df_accuracy_stats['price_next_day'], df_accuracy_stats['price_next_day_predicted'])
            direction_pct = df_accuracy_stats['direction_match'].sum() / df_accuracy_stats.shape[0]
            metrics_df['r2'].append(r2), metrics_df['direction_accuracy'].append(direction_pct) 
            # we are only intereseted in the validation set
            if subset[1] == 'validation':
                print('{}\tR2 is {:.1%} with {:.1%} direction match'.format(subset[0], r2, direction_pct))
        # output the data
        dashboard_df.to_csv('../dash_app/data/predictions.csv', index=False)
        pd.DataFrame(metrics_df).to_csv('../dash_app/data/metrics.csv', index=False)
        print('\nDashboard data refreshed')

# button
model_train_button = Button(description="Train model")
model_train_button_output = Output()
model_train_button.on_click(train_model)
