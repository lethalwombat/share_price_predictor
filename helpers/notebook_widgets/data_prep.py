import sys
sys.path.append('/helpers')
import pandas as pd
from os import listdir
from ipywidgets import Dropdown, Button, Output
from IPython.display import clear_output
from dataframes import df_reshape, add_target, rolling_max, cumulative_max, increase_decline_streak, previous_swing, rolling_mean

# widget options
_downloaded_files = sorted([f.split(".csv")[0] for f in listdir('/data') if f[0:8] == 'download'])

# set up notebook selectors
selectors = {
    'file' : {
        'description' : 'File:',
        'options' : _downloaded_files,
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

# prep features buttton
def prep_features(*args):
    with prep_features_button_output:
        clear_output()
        # import the selected file
        selected_file = selectors['file']['display'].value
        selected_download = (
            pd.read_csv(f'/data/{selected_file}.csv', parse_dates=['Date'])
            .reset_index(drop=True)
        )
        stock_codes = selected_download['stock_code'].unique().tolist()
        print('Imported {:,} records from {}.csv'.format(selected_download.shape[0], selected_file))
        print('Stock codes included:\n\t{}'.format('\n\t'.join(stock_codes)))
        # reshape the data to contain a record for each day, e.g. add weekends and public holidays
        selected_download = selected_download.pipe(df_reshape)
        print('Upsampled to {:,} records'.format(selected_download.shape[0]))
        # calculate the target `adj_close_next_day`
        selected_download = (
            selected_download
            .pipe(add_target)
        )
        print('Target variable added to {:,} records'.format(selected_download.shape[0]))
        # calculate `1 or 0` flag if the price is the highest in 5, 10 and 30 days, e.g. `highest_5`, `highest_10` and `highest_30`
        # calculate `1 or 0` flag if the price is the highest ever or cumulative max, e.g. `highest_ever`
        selected_download = (
            selected_download
            .pipe(rolling_max, 'Adj Close', 5)
            .pipe(rolling_max, 'Adj Close', 10)
            .pipe(rolling_max, 'Adj Close', 30)
            .pipe(cumulative_max, 'Adj Close')
            )
        # calculate date increase and decline streaks, e.g. number of days the price has been increasing `increase_streak` or declining `decline_streak`
        selected_download = (
            selected_download
            .pipe(increase_decline_streak, 'Adj Close')
        )
        # calculate date features `is_monday` and `is_friday`
        selected_download = (
            selected_download
            .assign(is_monday=selected_download['Date'].dt.weekday.apply(lambda ser : 1 if ser == 0 else 0))
            .assign(is_friday=selected_download['Date'].dt.weekday.apply(lambda ser : 1 if ser == 4 else 0))    
            )
        # calculate difference between the High and Low price for the previous day `previous_swing`
        selected_download = (
            selected_download
            .pipe(previous_swing, ('High', 'Low'))
        )
        # calculate rolling means
        selected_download = (
            selected_download
            .pipe(rolling_mean, 'adj_close_next_day', 2)
            .pipe(rolling_mean, 'adj_close_next_day', 3)
            .pipe(rolling_mean, 'adj_close_next_day', 5)
            .pipe(rolling_mean, 'adj_close_next_day', 7)            
        )
        print('Features calculated for {:,} records'.format(selected_download.shape[0]))
        # save the features into `/data`
        # generate a file name
        _ = lambda x : 'features_' + x.split('download_')[1] + '.csv'
        features_file_name = _(selectors['file']['display'].value)
        # output the file
        selected_download\
            .drop(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])\
            .loc[~selected_download['adj_close_next_day'].isna()]\
            .reset_index(drop=True)\
            .to_csv(f'../data/{features_file_name}', index=False)
        print('File saved as:\n\t{}'.format(features_file_name))

# button
prep_features_button = Button(description="Prepare features")
prep_features_button_output = Output()
prep_features_button.on_click(prep_features)
