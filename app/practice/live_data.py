import os
from dotenv import load_dotenv
import asyncio
import json
import redis
import psycopg2
from alpaca_trade_api.stream import Stream
import sys
from datetime import datetime

# Load .env file
load_dotenv()

# Alpaca credentials
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"
SYMBOL = "AAPL"

# Redis connection
r = redis.Redis(host="localhost", port=6379, db=0)

# PostgreSQL connection
try:
    pg_conn = psycopg2.connect(
        dbname="trading_simulator",
        user="postgres",  # change if different
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port="5432"
    )
    pg_conn.autocommit = True
    pg_cursor = pg_conn.cursor()
    print("✅ Connected to PostgreSQL.")
except Exception as e:
    print(f"❌ PostgreSQL connection failed: {e}")
    sys.exit(1)

# Save bar to Redis + Postgres
async def on_bar(bar):
    if isinstance(bar.timestamp, int):  # nanoseconds → datetime
        timestamp = datetime.fromtimestamp(bar.timestamp / 1e9)
    else:
        timestamp = bar.timestamp

    print(f"📊 New bar: {bar.symbol} at {timestamp} | Close={bar.close}")

    # Save to Redis
    bar_data = {
        "timestamp": str(timestamp),
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume
    }
    r.set(f"bar:{bar.symbol}", json.dumps(bar_data))
    print(f"💾 Cached bar for {bar.symbol} in Redis.")

    # Save to PostgreSQL
    try:
        pg_cursor.execute("""
            INSERT INTO bars (symbol, timestamp, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (bar.symbol, timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume))
        print(f"✅ Inserted into PostgreSQL.")
    except Exception as e:
        print(f"❌ Error inserting bar into PostgreSQL: {e}")

# For testing — faster updates than bars
async def on_trade(trade):
    print(f"⚡ Trade: {trade.symbol} at {trade.price} (Size={trade.size})")

async def main():
    try:
        print("🔌 Connecting to Alpaca...")
        stream = Stream(API_KEY, API_SECRET, base_url=BASE_URL, data_feed="iex")

        # Subscribe
        stream.subscribe_trades(on_trade, SYMBOL)  # trades come fast
        stream.subscribe_bars(on_bar, SYMBOL)      # bars every 1 minute

        print(f"📡 Subscribed to {SYMBOL} trades + bars.")
        await stream._run_forever()

    except Exception as e:
        print(f"❌ Main loop error: {e}")

def shutdown():
    print("🛑 Shutting down...")
    try:
        pg_cursor.close()
        pg_conn.close()
        print("✅ PostgreSQL connection closed.")
    except:
        pass
    sys.exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        shutdown()
