import pandas as pd

def bars_to_df(bars):
    """
    Convert list of bars (dicts) to pandas DataFrame with datetime index.
    """
    df = pd.DataFrame(bars)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('open_time', inplace=True)
    # Sort ascending just in case
    df.sort_index(inplace=True)
    return df

def add_features(df):
    """
    Add common technical features:
    - Returns
    - Moving averages (5, 10)
    - Rolling std (volatility)
    """
    df['return'] = df['close'].pct_change()
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['volatility'] = df['return'].rolling(window=10).std()
    df.dropna(inplace=True)
    return df
