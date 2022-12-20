import pandas as pd
from datetime import datetime

def _yahoo_date(dt) -> str:
    '''Convert dates into the format Yahoo can understand'''
    _dt = datetime.strptime(dt, '%Y-%m-%d')
    return str(1622505600 + (_dt - datetime(2021, 6, 1)).days * 86400)
 
def _yahoo_request(stock_code, dt_from, dt_to) -> str:
    '''Construct a request for Yahoo'''
    return "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&includeAdjustedClose=true"\
        .format(stock_code, _yahoo_date(dt_from), _yahoo_date(dt_to))

def download_stock_data(stock_code, dt_from, dt_to) -> pd.DataFrame:
    '''Download the stock code data for the selected dates and return a DataFrame'''
    df = (
        pd.read_csv(_yahoo_request(stock_code, dt_from, dt_to), index_col=False, usecols=['Date', 'High', 'Low', 'Adj Close'], parse_dates=['Date'])
        # .assign(stock_code=stock_code)
    )
    return df
