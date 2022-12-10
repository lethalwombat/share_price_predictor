import pandas as pd

def rolling_max(df, col, periods) -> pd.DataFrame:
    '''Calculate a binary flag if the selected columns is the
    highest in periods of time '''
    df['_rolling_max_'] = df[col].rolling(periods).max()
    rolling_max_flag = (
        df
        .apply(lambda row : 1 if row[col] == row['_rolling_max_'] else 0, axis=1)
    )
    df[f'highest_{periods}'] = rolling_max_flag
    df = df.drop(columns=['_rolling_max_'])
    return df


def cumulative_max(df, col) -> pd.DataFrame:
    '''Calculate a binary flag if the selected columns is the
    highest ever '''
    df['_cumulative_max_'] = df[col].cummax()
    cumulative_max_flag = (
        df
        .apply(lambda row : 1 if row[col] == row['_cumulative_max_'] else 0, axis=1)
    )
    df[f'highest_ever'] = cumulative_max_flag
    df = df.drop(columns=['_cumulative_max_'])
    return df


def increase_decline_streak(df, col) -> pd.DataFrame:
    '''Calculate cumulative number of days the price has been in decline'''
    df['_diff_'] = df[col].diff().fillna(value=0.0)
    increase_streak = (
        df
        .apply(lambda row : 'event' if row['_diff_'] > 0 else 'non-event', axis=1)
    )
    decline_streak = (
        df
        .apply(lambda row : 'event' if row['_diff_'] < 0 else 'non-event', axis=1)
    )

    df['_increase_'], df['_decline_'] = increase_streak, decline_streak
    df = df.drop(columns=['_diff_'])
    for event_flag in ['increase', 'decline']:
        df[f'{event_flag}_streak'] = df[f'_{event_flag}_'].groupby((df[f'_{event_flag}_'] != df[f'_{event_flag}_'].shift()).cumsum()).cumcount() + 1
        df.loc[df[f'_{event_flag}_'] == 'non-event', f'{event_flag}_streak'] = 0
        df = df.drop(columns=[f'_{event_flag}_'])
    return df


def previous_swing(df, cols) -> pd.DataFrame:
    '''Calculate difference between the High and Low price for the previous period'''
    df['_high_'], df['_low_'] = df[cols[0]].shift(periods=1), df[cols[1]].shift(periods=1)
    previous_swing = (
        df
        .apply(lambda row : row['_high_'] / row['_low_'], axis=1)
        .fillna(value=1.0)
    )
    df = (
        df
        .assign(previous_swing=previous_swing)
        .drop(columns=['_high_', '_low_'])
    )
    return df
