import pandas as pd
from itertools import product
from dates import month_end

def df_reshape(df) -> pd.DataFrame:
    '''Add missing weekends and public holidays to the dataframe'''
    data = []
    for slice in product(df['stock_code'].unique(), df['subset'].unique()):
        subset_df = (
            df
            .query(f'stock_code == "{slice[0]}"')
            .query(f'subset == "{slice[1]}"')
            .reset_index(drop=True)
            )
        min_date = pd.to_datetime(subset_df['Date']).min().replace(day=1)
        max_date = month_end(pd.to_datetime(subset_df['Date']).max())
        new_dates = pd.DataFrame(
            {
                'Date' : pd.date_range(start=min_date, end=max_date, freq='D').to_series().reset_index(drop=True)
            })
        subset_df = (
            subset_df
            .merge(new_dates, how='right', left_on='Date', right_on='Date')
            .assign(stock_code=slice[0], subset=slice[1])
            .ffill(axis=0)
            .bfill(axis=0)
            )
        data.append(subset_df.copy())
    return pd.concat(data, ignore_index=True)


def add_target(df) -> pd.DataFrame:
    '''Calculate the target `adj_close_next_day`'''
    data = []
    for slice in product(df['stock_code'].unique(), df['subset'].unique()):
        subset_df = (
            df
            .query(f'stock_code == "{slice[0]}"')
            .query(f'subset == "{slice[1]}"')
            .reset_index(drop=True)
        )
        subset_df['adj_close_next_day'] = 1 / (subset_df['Adj Close'].pct_change(periods=-1) + 1)
        data.append(subset_df.copy())
    return pd.concat(data, ignore_index=True)


def rolling_max(df, col, periods) -> pd.DataFrame:
    '''Calculate a binary flag if the selected columns is the
    highest in periods of time '''
    data = []
    for slice in product(df['stock_code'].unique(), df['subset'].unique()):
        subset_df = (
            df
            .query(f'stock_code == "{slice[0]}"')
            .query(f'subset == "{slice[1]}"')
            .reset_index(drop=True)
        )
        subset_df['_rolling_max_'] = subset_df[col].rolling(periods).max()
        rolling_max_flag = (
            subset_df
            .apply(lambda row : 1 if row[col] == row['_rolling_max_'] else 0, axis=1)
        )
        subset_df[f'highest_{periods}'] = rolling_max_flag
        subset_df = subset_df.drop(columns=['_rolling_max_'])
        data.append(subset_df.copy())  
    return pd.concat(data, ignore_index=True)


def cumulative_max(df, col) -> pd.DataFrame:
    '''Calculate a binary flag if the selected columns is the
    highest ever '''
    data = []
    for slice in product(df['stock_code'].unique(), df['subset'].unique()):
        subset_df = (
            df
            .query(f'stock_code == "{slice[0]}"')
            .query(f'subset == "{slice[1]}"')
            .reset_index(drop=True)
        )
        subset_df['_cumulative_max_'] = subset_df[col].cummax()
        cumulative_max_flag = (
            subset_df
            .apply(lambda row : 1 if row[col] == row['_cumulative_max_'] else 0, axis=1)
        )
        subset_df[f'highest_ever'] = cumulative_max_flag
        subset_df = subset_df.drop(columns=['_cumulative_max_'])
        data.append(subset_df.copy())
    return pd.concat(data, ignore_index=True)


def increase_decline_streak(df, col) -> pd.DataFrame:
    '''Calculate cumulative number of days the price has been in decline'''
    data = []
    for slice in product(df['stock_code'].unique(), df['subset'].unique()):
        subset_df = (
            df
            .query(f'stock_code == "{slice[0]}"')
            .query(f'subset == "{slice[1]}"')
            .reset_index(drop=True)
        )
        subset_df['_diff_'] = subset_df[col].diff().fillna(value=0.0)
        increase_streak = (
            subset_df
            .apply(lambda row : 'event' if row['_diff_'] > 0 else 'non-event', axis=1)
            )
        decline_streak = (
            subset_df
            .apply(lambda row : 'event' if row['_diff_'] < 0 else 'non-event', axis=1)
            )
        subset_df['_increase_'], subset_df['_decline_'] = increase_streak, decline_streak
        subset_df = subset_df.drop(columns=['_diff_'])
        for event_flag in ['increase', 'decline']:
            subset_df[f'{event_flag}_streak'] = subset_df[f'_{event_flag}_']\
                .groupby((subset_df[f'_{event_flag}_'] != subset_df[f'_{event_flag}_'].shift()).cumsum()).cumcount() + 1
            subset_df.loc[subset_df[f'_{event_flag}_'] == 'non-event', f'{event_flag}_streak'] = 0
            subset_df = subset_df.drop(columns=[f'_{event_flag}_'])
        data.append(subset_df.copy())
    return pd.concat(data, ignore_index=True)


def previous_swing(df, cols) -> pd.DataFrame:
    '''Calculate difference between the High and Low price for the previous period'''
    data = []
    for slice in product(df['stock_code'].unique(), df['subset'].unique()):
        subset_df = (
            df
            .query(f'stock_code == "{slice[0]}"')
            .query(f'subset == "{slice[1]}"')
            .reset_index(drop=True)
        )     
        subset_df['_high_'], subset_df['_low_'] = subset_df[cols[0]].shift(periods=1), subset_df[cols[1]].shift(periods=1)
        previous_swing = (
            subset_df
            .apply(lambda row : row['_high_'] / row['_low_'], axis=1)
            .fillna(value=1.0)
            )
        subset_df = (
            subset_df
            .assign(previous_swing=previous_swing)
            .drop(columns=['_high_', '_low_'])
            )
        data.append(subset_df.copy())
    return pd.concat(data, ignore_index=True)


def rolling_mean(df, col, periods) -> pd.DataFrame:
    '''Calculate rolling mean for the selected dataframe column'''
    data = []
    for slice in product(df['stock_code'].unique(), df['subset'].unique()):
        subset_df = (
            df
            .query(f'stock_code == "{slice[0]}"')
            .query(f'subset == "{slice[1]}"')
            .reset_index(drop=True)
        )
        rolling_value = subset_df[col].rolling(periods)\
            .mean()\
            .shift(periods=1)
        subset_df[f'rolling_{periods}'] = rolling_value.combine_first(subset_df[col])
        data.append(subset_df.copy())
    return pd.concat(data, ignore_index=True)
