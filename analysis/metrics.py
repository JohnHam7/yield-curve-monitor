import pandas as pd
import time

def get_yield_data(fred, start_date='2000-01-01'):
    maturities = {
        '3M': 'GS3M', '1Y': 'GS1', '2Y': 'GS2',
        '5Y': 'GS5', '7Y': 'GS7', '10Y': 'GS10',
        '20Y': 'GS20', '30Y': 'GS30'
    }
    series_dict = {}
    for label, code in maturities.items():
        series_dict[label] = fred.get_series(code, observation_start=start_date)
        time.sleep(0.3)

    df = pd.DataFrame(series_dict).dropna()
    return df

def calculate_spread(curve_df):
    df = curve_df.copy()
    df['spread'] = df['10Y'] - df['2Y']
    df['inverted'] = df['spread'] < 0
    return df

def calculate_zscore(series, window=24):
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

def get_recession_data(fred, start_date='2000-01-01'):
    return fred.get_series('USREC', observation_start=start_date).fillna(0)