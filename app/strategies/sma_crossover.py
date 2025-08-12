import pandas as pd
import matplotlib.pyplot as plt

def sma_crossover_strategy(csv_path: str):
    # Load historical data
    df = pd.read_csv(csv_path, index_col='time', parse_dates=True)

    # Calculate SMAs
    df['SMA50'] = df['close'].rolling(window=50).mean()
    df['SMA200'] = df['close'].rolling(window=200).mean()

    print(f"Data length: {len(df)}")
    print(df[['SMA50', 'SMA200']].tail(10))


    # Generate signals
    df['signal'] = 0
    df.loc[df['SMA50'] > df['SMA200'], 'signal'] = 1  # Buy
    df.loc[df['SMA50'] < df['SMA200'], 'signal'] = -1 # Sell

    # Find crossover points (where signal changes)
    df['position'] = df['signal'].diff()

    # Buy signal: position changes from 0 or -1 to 1 (signal rising)
    buy_signals = df[(df['position'] == 1) | (df['position'] == 2)]

    # Sell signal: position changes from 0 or 1 to -1 (signal falling)
    sell_signals = df[(df['position'] == -1) | (df['position'] == -2)]


    print("Buy signals:\n", buy_signals.index)
    print("Sell signals:\n", sell_signals.index)

    return df

def plot_sma_signals(df):
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['close'], label='Close Price', alpha=0.5)
    plt.plot(df.index, df['SMA50'], label='SMA 50')
    plt.plot(df.index, df['SMA200'], label='SMA 200')

    # Plot buy signals
    buys = df[df['position'] == 1]
    plt.scatter(buys.index, df.loc[buys.index, 'close'], marker='^', color='g', label='Buy Signal', s=100)

    # Plot sell signals
    sells = df[df['position'] == -1]
    plt.scatter(sells.index, df.loc[sells.index, 'close'], marker='v', color='r', label='Sell Signal', s=100)

    plt.title('SMA Crossover Strategy Signals')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    csv_path = "C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/data/AAPL_historical.csv"  # Adjust path as needed
    df_signals = sma_crossover_strategy(csv_path)
    plot_sma_signals(df_signals)
