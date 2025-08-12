import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

def fetch_historical_data(symbol: str, timeframe: str = "1Day", limit: int = 365):
    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=limit)

    barset = api.get_bars(
        symbol, 
        timeframe, 
        start=start_dt.strftime('%Y-%m-%d'), 
        end=end_dt.strftime('%Y-%m-%d'),
        feed='iex'
    )

    data = []
    for bar in barset:
        data.append({
            "time": bar.t.isoformat(),
            "open": bar.o,
            "high": bar.h,
            "low": bar.l,
            "close": bar.c,
            "volume": bar.v
        })

    df = pd.DataFrame(data)
    df.set_index("time", inplace=True)
    return df

if __name__ == "__main__":
    symbol = "AAPL"
    df = fetch_historical_data(symbol)
    print(f"Fetched {len(df)} bars for {symbol}")

    # Make sure data directory exists
    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/{symbol}_historical.csv")
    print(f"Saved historical data to data/{symbol}_historical.csv")
