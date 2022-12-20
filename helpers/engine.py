import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from download import download_stock_data
from features import rolling_max, cumulative_max, increase_decline_streak, rolling_mean, simulate_price

def run_model(stock_code, training_year, training_data_size=1, learning_rate=0.15, n_estimators=150, model_type='GB') -> pd.DataFrame:
    # download the data and rename columns
    df = (
        download_stock_data(stock_code, f'{int(training_year)-training_data_size}-12-01', f'{int(training_year)+2}-01-30')
        .rename(columns={'Date' : 'date', 'Adj Close' : 'price_today'})
    )
    # split into training and validation
    df = (
        df
        .assign(subset=df['date'].apply(lambda ser : 'validation' if ser.year > int(training_year) else 'training'))
        )
    # add price from the previous and next day 
    df = (
        df
        .assign(price_next_day=df['price_today'].shift(periods=-1))
        .assign(price_yesterday=df['price_today'].shift(periods=1))
    )
    # calculate daily price increase
    df['price_increase_today'] = df['price_today'] / df['price_yesterday'] - 1
    df['price_increase_next_day'] = df['price_next_day'] / df['price_today'] - 1
    # calculate features
    df = (
        df
        .pipe(rolling_max, 'price_today', 5, 'price_highest')
        .pipe(rolling_max, 'price_today', 10, 'price_highest')
        .pipe(rolling_max, 'price_today', 30, 'price_highest')
        .pipe(cumulative_max, 'price_today', 'price_highest_ever')
        .pipe(rolling_max, 'price_increase_today', 5, 'increase_highest')
        .pipe(rolling_max, 'price_increase_today', 10, 'increase_highest')
        .pipe(rolling_max, 'price_increase_today', 30, 'increase_highest')
        .pipe(cumulative_max, 'price_increase_today', 'increase_highest_ever')
        .pipe(increase_decline_streak, 'price_today')
        .assign(price_swing_today=df['High'] / df['Low'])
        .drop(columns=['High', 'Low'])
        .pipe(rolling_mean, 'price_today', 2, 'price_rolling_mean')
        .pipe(rolling_mean, 'price_today', 3, 'price_rolling_mean')
        .pipe(rolling_mean, 'price_today', 5, 'price_rolling_mean')
        .pipe(rolling_mean, 'price_today', 7, 'price_rolling_mean')
        .pipe(rolling_mean, 'price_increase_today', 2, 'increase_rolling_mean')
        .pipe(rolling_mean, 'price_increase_today', 3, 'increase_rolling_mean')
        .pipe(rolling_mean, 'price_increase_today', 5, 'increase_rolling_mean')
        .pipe(rolling_mean, 'price_increase_today', 7, 'increase_rolling_mean')        
    )
    # remove records outside of the training and prediction window
    df = (
        df
      .loc[df['date'].dt.year.isin(range(int(training_year)+1, int(training_year)-training_data_size, -1))]
      .reset_index(drop=True)
      )

    # train the model
    model_target = 'price_increase_next_day'
    model_features = [
        'price_increase_today',
        'price_highest_5', 'price_highest_10', 'price_highest_30', 'price_highest_ever',
        'increase_highest_5', 'increase_highest_10', 'increase_highest_30', 'increase_highest_ever',
        'increase_rolling_mean_2', 'increase_rolling_mean_3', 'increase_rolling_mean_5', 'increase_rolling_mean_7'
    ]
    X_train = (
        df
        .query('subset=="training"')
        [model_features]
    )
    y_train = (
        df
        .query('subset=="training"')
        [model_target]
    )
    X_test = (
        df
        .query('subset=="validation"')
        [model_features]
    )
    y_test = (
        df
        .query('subset=="validation"')
        [model_target]
    )
    # scale the inputs
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    # algo types
    model_types = {
        'GB' : GradientBoostingRegressor(learning_rate=learning_rate, n_estimators=n_estimators, max_depth=3),
        'LinReg' : LinearRegression() 
    }
    reg = model_types.get(model_type)
    # fit the model
    reg.fit(X_train_scaled, y_train)
    # fit predictions
    X_train['prediction'], X_test['prediction'] = reg.predict(X_train_scaled), reg.predict(scaler.transform(X_test))
    # print accuracy metrics
    r2_train = r2_score(y_train, X_train['prediction'])
    r2_validation = r2_score(y_test, X_test['prediction'])
    print('\nR2 train is {:.1%}\nR2 validation is {:.1%}'.format(r2_train, r2_validation))
    # add predictions to the input
    df = (
        df
        .merge(pd.concat([
            X_train[['prediction']], X_test[['prediction']]
        ]), how='left', left_index=True, right_index=True)
        [['date', 'price_today', 'price_next_day', model_target, 'prediction', 'subset']]
        .rename(columns={model_target : 'actual'})
        .pipe(simulate_price)
        .assign(r2_train=r2_train)
        )
    return df
