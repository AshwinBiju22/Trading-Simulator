import pandas as pd

# Load your AAPL historical data
csv_path = r"C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/data/AAPL_historical.csv"
df_original = pd.read_csv(csv_path, index_col='time', parse_dates=True)

def run_backtest(df, short_window, long_window):
    df = df.copy()
    df['SMA_short'] = df['close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['close'].rolling(window=long_window).mean()

    df['signal'] = 0
    df.loc[df['SMA_short'] > df['SMA_long'], 'signal'] = 1
    df.loc[df['SMA_short'] < df['SMA_long'], 'signal'] = -1

    # Shift signals so trades execute next day
    df['position'] = df['signal'].shift()

    initial_cash = 100000
    cash = initial_cash
    position = 0
    trades = 0

    for i in range(len(df)):
        if df['position'].iloc[i] == 1 and position == 0:
            position = cash / df['close'].iloc[i]  # Buy
            cash = 0
            trades += 1
        elif df['position'].iloc[i] == -1 and position > 0:
            cash = position * df['close'].iloc[i]  # Sell
            position = 0
            trades += 1

    if position > 0:  # Close any open position at end
        cash = position * df['close'].iloc[-1]

    total_profit = cash - initial_cash
    return total_profit, trades

results = []

# Try short SMA from 5 to 30, long SMA from 20 to 200
for short_window in range(5, 31, 5):  # step of 5
    for long_window in range(20, 201, 10):  # step of 10
        if short_window >= long_window:
            continue
        profit, trades = run_backtest(df_original, short_window, long_window)
        results.append((short_window, long_window, profit, trades))

# Create a results DataFrame
results_df = pd.DataFrame(results, columns=['Short_SMA', 'Long_SMA', 'Profit', 'Trades'])

# Sort by best profit
results_df = results_df.sort_values(by='Profit', ascending=False)

print("\nTop 10 SMA combinations:")
print(results_df.head(10))
