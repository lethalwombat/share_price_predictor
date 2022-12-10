import sys
sys.path.append('/helpers')
import pandas as pd
from os import listdir
from ipywidgets import Dropdown

# widget options
_downloaded_files = sorted([f.split(".csv")[0] for f in listdir('/data') if f[0:8] == 'download'])

# for each downloaded file we need to understand which stock codes exists in it
_stock_codes = {}
for file_name in _downloaded_files:
    _stock_codes['file'] = file_name
    _stock_codes[file_name] = pd.read_csv(f'/data/{file_name}.csv', usecols=['stock_code'])\
        ['stock_code']\
        .unique()\
        .tolist()

# set up notebook selectors
selectors = {
    'file' : {
        'description' : 'File:',
        'options' : _downloaded_files,
        'type' : Dropdown
    },
    'stock_code' : {
        'description' : 'Stock code:',
        'options' : _stock_codes[_downloaded_files[0]],
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

# update stock code values interactively
def update_stock_codes(*args):
    selectors['stock_code']['display'].options = _stock_codes[selectors['file']['display'].value]

selectors['file']['display'].observe(update_stock_codes)