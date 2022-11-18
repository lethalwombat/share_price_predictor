import sys
sys.path.append('/helpers')
from ipywidgets import Dropdown, SelectMultiple, Button, Output
from IPython.display import clear_output
import pandas as pd
from datetime import datetime, timedelta
from dates import month_add
from yahoo import download_stock_data

# widget options
_start_periods = [str(i) for i in range(2010, 2021)]
_training_data = ["{} months".format(i) for i in range(3, 15, 3)]
_validation_data = ["{} months".format(i) for i in range(3, 15, 3)]
_stock_codes = ['IVV', 'IVV.AX', 'IJR', 'VAS.AX', 'VAP.AX', 'ASX.AX', 'VGS.AX', 'VAF.AX']

# set up notebook selectors
selectors = {
    'start_period' : {
        'description' : 'Start year:',
        'options' : _start_periods,
        'type' : Dropdown
    },
    'training_data' : {
        'description' : 'Training:',
        'options' : _training_data,
        'type' : Dropdown
    },
    'validation_data' : {
        'description' : 'Validation:',
        'options' : _validation_data,
        'type' : Dropdown
    },
    'stock_codes' : {
        'description' : 'Stock codes:',
        'options' : sorted(set(_stock_codes)),
        'type' : SelectMultiple
    }
}

# set up widget default values
for s in selectors:
    selector_value = selectors[s]['options'][0]
    # stock codes widget values
    if s == 'stock_codes':
        selector_value = [selectors[s]['options'][0]]
    # set up the widget for display
    selectors[s]['display'] = selectors[s]['type'](
        description=selectors[s]['description'],
        options=selectors[s]['options'],
        value=selector_value
    )

# check download settings
def check_settings(*args):
    with check_button_output:
        clear_output()
        print('Start year:\n\t{}'.format(selectors['start_period']['display'].value))
        print('Training data:\n\t{}'.format(selectors['training_data']['display'].value))
        print('Validation data:\n\t{}'.format(selectors['validation_data']['display'].value))
        print('Stock codes selected:\n\t{}'.format(' '.join(selectors['stock_codes']['display'].value)))

# check download settings button
check_button = Button(description="Check settings")
check_button_output = Output()
check_button.on_click(check_settings)

# file timestamp
timestamp = lambda : datetime.now().strftime("%Y%m%d_%H%M%S")

# check download settings
def download(*args):
    with download_button_output:
        clear_output()
        _df = []
        for stock in selectors['stock_codes']['display'].value:
            _dt_from = '{}-01-01'.format(selectors['start_period']['display'].value)
            _dt_to = month_add(_dt_from, int(selectors['training_data']['display'].value.split('months')[0]))
            print('Downloading {} data from {} to {}'.format(stock, _dt_from, _dt_to))
            # download training data first
            _chunk = (
                download_stock_data(stock, _dt_from, _dt_to)
                .assign(subset='training')
            )
            _df.append(_chunk)
            # now we do the same for validation data
            _dt_from = (datetime.strptime(_dt_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            _dt_to = month_add(_dt_from, int(selectors['validation_data']['display'].value.split('months')[0]))
            print('Downloading {} data from {} to {}'.format(stock, _dt_from, _dt_to))
            _chunk = (
                download_stock_data(stock, _dt_from, _dt_to)
                .assign(subset='validation')
            )
            _df.append(_chunk)

        # convert downloaded data to DataFrame
        pd.concat(_df, ignore_index=True).to_csv('../data/download_{}.csv'.format(timestamp()))

# check download settings button
download_button = Button(description="Download")
download_button_output = Output()
download_button.on_click(download)