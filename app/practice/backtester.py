import pandas as pd
import matplotlib.pyplot as plt

# Function to generate trading signals
def generate_signals(df):
    # Calculate shorter-term SMAs for more frequent trades
    df['SMA10'] = df['close'].rolling(window=10).mean()
    df['SMA30'] = df['close'].rolling(window=30).mean()

    # Generate signals: 1 for buy, -1 for sell, 0 for hold
    df['signal'] = 0
    df.loc[df['SMA10'] > df['SMA30'], 'signal'] = 1
    df.loc[df['SMA10'] < df['SMA30'], 'signal'] = -1

    return df

# Load historical CSV
csv_path = r"C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/data/AAPL_historical.csv"
df = pd.read_csv(csv_path, parse_dates=True)

# Make sure column names are clean
df.columns = df.columns.str.strip().str.lower()

# Generate signals
df = generate_signals(df)

# Debugging: See how many of each signal type
print("Signal value counts:")
print(df['signal'].value_counts())

# Backtest logic
initial_cash = 10000
cash = initial_cash
position = 0
for i in range(len(df)):
    if df['signal'].iloc[i] == 1 and position == 0:
        # Buy one unit
        position = cash / df['close'].iloc[i]
        cash = 0
    elif df['signal'].iloc[i] == -1 and position > 0:
        # Sell all
        cash = position * df['close'].iloc[i]
        position = 0

# Final portfolio value
final_value = cash + (position * df['close'].iloc[-1])
profit = final_value - initial_cash

print(f"Total trades: {(df['signal'].diff() != 0).sum()}")
print(f"Total profit: {profit:.2f}")


# === 5. Plot ===
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['close'], label='Close Price', color='black', alpha=0.6)
plt.plot(df.index, df['SMA10'], label='SMA10', color='blue', alpha=0.8)
plt.plot(df.index, df['SMA30'], label='SMA30', color='orange', alpha=0.8)

# Plot buy/sell markers
buy_signals = df[(df['signal'] == 1) & (df['signal'].shift(1) != 1)]
sell_signals = df[(df['signal'] == -1) & (df['signal'].shift(1) != -1)]

plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', s=100, label='Buy Signal')
plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', s=100, label='Sell Signal')

plt.title('SMA Crossover Strategy Backtest')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()